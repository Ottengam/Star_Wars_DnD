from django.urls import path
from . import views

app_name = 'mechanics'

urlpatterns = [
    # URL: ://site.com
    path('rules/', views.RulesHubView.as_view(), name='rules_hub'),
    path('rules/<slug:slug>/', views.RuleDetailView.as_view(), name='rule_detail'),
    path('skills/<int:skill_id>/perks/', views.SkillPerksDetailView.as_view(), name='skill_perks')
]
