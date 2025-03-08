from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
# Modèle utilisateur : Infirmiers et recruteurs

class CustomUser(AbstractUser):
    specialty = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(default=0)
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
        ('es', 'Español'),
    ]
    
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')

    def __str__(self):
        return self.username

    def send_welcome_message(self):
        # Messages en fonction de la langue
        messages = {
            'fr': _("Bienvenue ! Votre compte a été créé avec succès."),
            'en': _("Welcome! Your account has been successfully created."),
            'es': _("¡Bienvenido! Su cuenta ha sido creada con éxito."),
        }

        message = messages.get(self.language, messages['fr'])  # Français par défaut

        # Envoyer le message par e-mail
        from django.core.mail import send_mail
        send_mail(
            subject=_("Welcome to Our Platform"),
            message=message,
            from_email="your_email@example.com",  # Remplacez par votre adresse e-mail
            recipient_list=[self.email],
            fail_silently=False,
        )

        return message


# Modèle des offres d’emploi
class JobOffer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=50, choices=[('CDI', 'CDI'), ('CDD', 'CDD'), ('Intérim', 'Intérim')])
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="job_offers")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

# Modèle des candidatures
class Application(models.Model):
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="applications")
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField()
    status = models.CharField(max_length=50, default="Pending")  # Pending, Accepted, Rejected
    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.applicant.username} - {self.job_offer.title}"