from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import (
    CASCADE,
    CharField,
    CheckConstraint,
    DateTimeField,
    EmailField,
    ForeignKey,
    ManyToManyField,
    Model,
    Q,
    SlugField,
    TextField,
)
from django.db.models.fields import IntegerField, URLField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from location_field.forms.plain import PlainLocationField
from slugify.slugify import slugify

from stavros.users.managers import UserManager
from stavros.users.utils.choices import COURSE_OPTIONS, ORGANIZATION_TYPES


class User(AbstractUser):
    """
    Default custom user model for Stavros.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    subscribed_tags = ManyToManyField("Tag")
    subscribed_organizations = ManyToManyField("Organization")
    contacts = ManyToManyField("Contact", blank=True, related_name="contacts")
    # is teacher is if they are in the teacher group
    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        # user cannot be teacher and student
        constraints = [
            CheckConstraint(
                check=Q(is_student=True) | Q(is_teacher=True),
                name="teacher_or_student",
            )
        ]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Class(Model):
    name = CharField(max_length=255)
    subject = CharField(max_length=255, choices=COURSE_OPTIONS)
    grade_level = IntegerField(choices=[(i, i) for i in range(9, 13)])
    teacher = ForeignKey(User, on_delete=CASCADE, related_name="classes_teaching")
    students = ManyToManyField(User, related_name="classes_attending", blank=True)


class StudentProfile(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name="student_profile")
    birth_date = DateTimeField()
    graduating_year = CharField(max_length=255, choices=[(i, i) for i in range(2022, 2030)])
    student_id = CharField(unique=True, max_length=9)  # 9 digit student id
    notes = TextField()
    guidance_counselor = ForeignKey(User, on_delete=CASCADE, related_name="students", null=True, blank=True)
    classes_taken = ManyToManyField("Class")


class Resource(Model):
    title = CharField(max_length=255)
    additional_info = TextField()
    link = URLField(null=True, blank=True)
    tags = ManyToManyField("Tag", related_name="resources")


class Contact(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name="info")
    position = CharField(max_length=255)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",  # only allow proper phone numbers to be entered
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = CharField(validators=[phone_regex], max_length=17, blank=True)
    name = CharField(max_length=255)
    industry = CharField(max_length=255)
    event_type = CharField(max_length=255)
    resources = TextField()
    tags = ManyToManyField("Tag", blank=True, related_name="contacts")


class Announcement(Model):
    slug = SlugField(unique=True, editable=False, null=True, blank=True)
    title = CharField(max_length=255)
    content = TextField()
    date_posted = DateTimeField(auto_now_add=True, editable=False)
    tags = ManyToManyField("Tag", related_name="announcements")
    organization = ForeignKey("Organization", on_delete=CASCADE, related_name="announcements")

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:  # only on creation
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Organization(Model):
    name = CharField(max_length=200)
    slug = SlugField(unique=True, editable=False, null=True, blank=True)
    category = CharField(max_length=255, choices=[(i, i) for i in ORGANIZATION_TYPES])
    event_type = CharField(max_length=255)
    resources = ManyToManyField("Resource", related_name="organizations", blank=True)
    contacts = ManyToManyField("Contact", blank=True)
    tags = ManyToManyField("Tag", related_name="organizations")

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:  # only on creation
            self.slug = slugify(self.name)  # replace spaces with hyphens and other unicode changes.
        super().save(*args, **kwargs)


class Event(Model):
    name = CharField(max_length=255)
    info = TextField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    organization = ForeignKey(Organization, on_delete=CASCADE, related_name="events")
    city = CharField(max_length=40)
    location = PlainLocationField(based_fields=["city"], zoom=7)
    tags = ManyToManyField("Tag", related_name="events")
    attendees = ManyToManyField(User, related_name="events", blank=True)


class Tag(Model):
    name = CharField(max_length=255)
