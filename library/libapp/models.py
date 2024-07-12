from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[("member", "member"), ("staff", "staff")],
        default="member",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.email


class Book(models.Model):
    genrechoice = [
        ("education", "Education"),
        ("comics", "Comics"),
        ("biography", "Biography"),
        ("history", "History"),
        ("science", "Science"),
        ("engineering", "Engineering"),
        ("medicine", "Medicine"),
        ("commerce", "Commerce"),
        ("arts", "Arts"),
        ("maths", "Maths"),
        ("language", "Language"),
    ]
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    genre = models.CharField(max_length=30, choices=genrechoice, default="education")
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]


class BorrowedBooks(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_return = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.due_date = self.borrow_date + timedelta(days=10)
        super(BorrowedBooks, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-borrow_date"]


class BookReservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
