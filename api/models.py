from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
# Modèle utilisateur : Infirmiers et recruteurs

class CustomUser(AbstractUser):
    SPECIALTY_CHOICES = [
    ('soins_generaux', _('Soins généraux / General Care / Cuidados gerais')),
    ('anesthesie', _('Infirmier anesthésiste / Nurse Anesthetist / Enfermeiro anestesista')),
    ('soins_intensifs', _('Soins intensifs / Intensive Care / Cuidados intensivos')),
    ('pediatrique', _('Pédiatrique / Pediatric / Pediátrico')),
    ('sante_mentale', _('Santé mentale / Mental Health / Saúde mental')),
    ('geriatrie', _('Gériatrie / Geriatrics / Geriatria')),
    ('oncologie', _('Oncologie / Oncology / Oncologia')),
    ('cardiologie', _('Cardiologie / Cardiology / Cardiologia')),
    ('soins_palliatifs', _('Soins palliatifs / Palliative Care / Cuidados paliativos')),
    ('chirurgie', _('Chirurgie / Surgery / Cirurgia')),
    ('obstetrique', _('Obstétrique / Obstetrics / Obstetrícia')),
    ('neonatalogie', _('Néonatalogie / Neonatology / Neonatologia')),
    ('soins_communautaires', _('Soins communautaires / Community Care / Cuidados comunitários')),
    ('pratique_avancee', _('Pratique avancée / Advanced Practice / Prática avançada')),
    ('education_sante', _('Éducation à la santé / Health Education / Educação em saúde')),
]



    specialty = models.CharField(max_length=255, choices=SPECIALTY_CHOICES)
  
    experience_years = models.PositiveIntegerField(default=0)
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
        ('es', 'Español'),
    ]
    
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    cv = models.FileField(upload_to='pdf_contrats/', null=True, blank=True)
    def __str__(self):
        return self.username

    def send_welcome_message(self,username):
    # Messages en fonction de la langue
     messages = {
        'fr': _("Cher {username}, bienvenue ! Votre compte a été créé avec succès."),
        'en': _("Dear {username}, welcome! Your account has been successfully created."),
        'es': _("Estimado/a {username}, ¡bienvenido! Su cuenta ha sido creada con éxito."),
    }
    
     subjects = {
        'fr': _("Bienvenue sur notre plateforme E&R GLOBALNURSES"),
        'en': _("Welcome to Our Platform E&R GLOBALNURSES"),
        'es': _("Bienvenido a nuestra plataforma E&R GLOBALNURSES"),
     }

      # Personnaliser les messages avec le nom d'utilisateur
     message = messages.get(self.language, messages['fr']).format(username=username)
     subject = subjects.get(self.language, subjects['fr'])  # Français par défaut
    # Envoyer le message par e-mail
     from django.core.mail import send_mail
     send_mail(
        subject=subject,
        message=message,
        from_email="urbainpatient5@gmail.com",  # Remplacez par votre adresse e-mail
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
    motivation_letter = models.FileField(upload_to='pdf_contrats/', null=True, blank=True) # C
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