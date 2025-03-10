# Generated by Django 5.1.7 on 2025-03-09 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_customuser_language_recruiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('candidate', 'Candidate'), ('recruiter', 'Recruiter'), ('candidate_fr', 'Candidat'), ('recruiter_fr', 'Recruteur'), ('candidate_es', 'Candidato'), ('recruiter_es', 'Reclutador'), ('candidate_ro', 'Candidat'), ('recruiter_ro', 'Recrutator')], default='candidate', max_length=20),
        ),
    ]
