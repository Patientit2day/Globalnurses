from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

# Modèle utilisateur : Infirmiers et recruteurs


class CustomUser(AbstractUser):
    SPECIALTY_CHOICES = [
         ('soins_generaux', _('Soins généraux / General Care / Cuidados gerais / Îngrijiri generale')),
        ('anesthesie', _('Infirmier anesthésiste / Nurse Anesthetist / Enfermeiro anestesista / Asistent anestezist')),
        ('soins_intensifs', _('Soins intensifs / Intensive Care / Cuidados intensivos / Îngrijiri intensive')),
        ('pediatrique', _('Pédiatrique / Pediatric / Pediátrico / Pediatric')),
        ('sante_mentale', _('Santé mentale / Mental Health / Saúde mental / Sănătate mintală')),
        ('geriatrie', _('Gériatrie / Geriatrics / Geriatria / Geriatrie')),
        ('oncologie', _('Oncologie / Oncology / Oncologia / Oncologie')),
        ('cardiologie', _('Cardiologie / Cardiology / Cardiologia / Cardiologie')),
        ('soins_palliatifs', _('Soins palliatifs / Palliative Care / Cuidados paliativos / Îngrijiri paliative')),
        ('chirurgie', _('Chirurgie / Surgery / Cirurgia / Chirurgie')),
        ('obstetrique', _('Obstétrique / Obstetrics / Obstetrícia / Obstetrică')),
        ('neonatalogie', _('Néonatalogie / Neonatology / Neonatologia / Neonatologie')),
        ('soins_communautaires', _('Soins communautaires / Community Care / Cuidados comunitários / Îngrijiri comunitare')),
        ('pratique_avancee', _('Pratique avancée / Advanced Practice / Prática avançada / Practică avansată')),
        ('education_sante', _('Éducation à la santé / Health Education / Educação em saúde / Educație pentru sănătate')),
    ]

    specialty = models.CharField(max_length=255, choices=SPECIALTY_CHOICES)
    experience_years = models.PositiveIntegerField(default=0)
    
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
        ('es', 'Español'),
        ('ro', 'Română'),  # Ajout du roumain
    ]
    
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')  # Changement de la langue par défaut à l'anglais
    cv = models.FileField(upload_to='pdf_contrats/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Champ ajouté
    address = models.CharField(max_length=255, blank=True, null=True)  # Champ d'adresse ajouté
    nationality = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return self.username

    def send_welcome_message(self, username):
        # Messages en fonction de la langue
        messages = {
            'fr': _("Cher/ère {username}, bienvenue ! Votre compte a été créé avec succès."),
            'en': _("Dear {username}, welcome! Your account has been successfully created."),
            'es': _("Estimado/a {username}, ¡bienvenido! Su cuenta ha sido creada con éxito."),
            'ro': _("Dragă {username}, bun venit! Contul tău a fost creat cu succes."),
        }

        subjects = {
            'fr': _("Bienvenue sur notre plateforme E&R GLOBALNURSES"),
            'en': _("Welcome to Our Platform E&R GLOBALNURSES"),
            'es': _("Bienvenido a nuestra plataforma E&R GLOBALNURSES"),
            'ro': _("Bun venit pe platforma noastră E&R GLOBALNURSES"),
        }

        # Personnaliser les messages avec le nom d'utilisateur
        message = messages.get(self.language, messages['en']).format(username=username)
        subject = subjects.get(self.language, subjects['en'])  # Anglais par défaut

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


# class Recruiter(models.Model):
#     RECRUITER_TYPE_CHOICES = [
#         ('hospital', 'Hôpital/Clinique'),
#         ('agency', 'Agence de recrutement'),
#         ('other', 'Autre établissement de santé'),
#     ]

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Lier à un compte utilisateur
#     organization = models.CharField(max_length=255)  # Nom de l'organisation
#     phone_number = models.CharField(max_length=20, blank=True, null=True)  # Champ de numéro de téléphone
#     address = models.CharField(max_length=255, blank=True, null=True)  # Champ d'adresse
#     recruiter_type = models.CharField(max_length=10, choices=RECRUITER_TYPE_CHOICES)  # Type de recruteur
#     created_at = models.DateTimeField(auto_now_add=True)  # Date de création

#     def __str__(self):
#         return f"{self.organization} ({self.get_recruiter_type_display()})"
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
    motivation_letter = models.FileField(upload_to='pdf_contrats/', null=True, blank=True) # C
    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.applicant.username} - {self.job_offer.title}"