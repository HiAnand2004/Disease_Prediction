from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .predictor import predict_disease
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import User
from django.core.mail import send_mail
from django.contrib import messages



def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    return render(request, 'healthadvisor/home.html', {'user': request.user})



def logout_view(request):
    logout(request)
    return redirect('login') 

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Changed from 'dashboard' to 'home'

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to HOME after registration
    else:
        form = RegistrationForm()
    return render(request, 'healthadvisor/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():  # New check
            messages.error(request, "Email not registered")
            return redirect('login')
            
        user = authenticate(request, email=email, password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Invalid password")
    return render(request, 'healthadvisor/login.html')


from django.http import JsonResponse
from .test import predict_disease  

def predict_view(request):
    if request.method == "POST":
        symptoms = request.POST.get("symptoms").strip().lower().split(',')
        symptoms = [symptom.strip() for symptom in symptoms if symptom.strip()]

        if len(symptoms) >= 2:
            predictions = predict_disease(symptoms)
            disease = list(predictions.values())[0]
            confidence = calculate_confidence(symptoms)  # Implement this function
            
            # Disease-specific recommendations
            recommendations = get_recommendations(disease, symptoms)
            
            return JsonResponse({
                'disease': disease,
                'confidence': confidence,
                'recommendations': recommendations,
                'severity': assess_severity(disease)  # Add severity level
            })
        else:
            return JsonResponse({'error': 'Please enter at least two symptoms.'})

    return render(request, 'healthadvisor/prediction.html')

def get_recommendations(disease, symptoms):
    """Return disease-specific recommendations with symptom-based customization"""
    recommendations_map = {
        'asthma': [
            "Use prescribed inhalers as directed",
            "Avoid known triggers (pollen, dust, smoke)",
            "Practice breathing exercises",
            "Seek emergency care if experiencing severe breathing difficulty",
            "Monitor peak flow readings regularly"
        ],
        'diabetes': [
            "Monitor blood sugar levels regularly",
            "Follow prescribed medication/insulin regimen",
            "Maintain a balanced diet with controlled carbohydrates",
            "Check feet daily for cuts or sores",
            "Schedule regular eye exams"
        ],
        'hypertensive heart disease': [
            "Take blood pressure medications as prescribed",
            "Reduce sodium intake to <1500mg daily",
            "Monitor blood pressure twice daily",
            "Limit alcohol to 1 drink per day",
            "Report chest pain or severe shortness of breath immediately"
        ],
        'coronary atherosclerosis': [
            "Take prescribed statins and antiplatelet medications",
            "Follow cardiac rehabilitation program",
            "Adopt heart-healthy Mediterranean diet",
            "Monitor for chest pain (angina) symptoms",
            "Call emergency services for crushing chest pain lasting >5 minutes"
        ],
        'chronic obstructive pulmonary disease (copd)': [
            "Use bronchodilators as prescribed",
            "Practice pursed-lip breathing techniques",
            "Get annual flu and pneumonia vaccines",
            "Avoid smoke and air pollution",
            "Consider pulmonary rehabilitation"
        ],
        'pneumonia': [
            "Complete full course of prescribed antibiotics",
            "Stay hydrated and get plenty of rest",
            "Use humidifier to ease breathing",
            "Seek immediate care if lips turn blue or breathing becomes labored",
            "Monitor oxygen levels if pulse oximeter available"
        ],
        'urinary tract infection': [
            "Drink plenty of water to flush bacteria",
            "Complete full antibiotic course",
            "Avoid caffeine and alcohol during infection",
            "Use heating pad for discomfort",
            "Consult doctor if fever develops or symptoms worsen after 2 days"
        ],
        'gastroesophageal reflux disease (gerd)': [
            "Elevate head of bed 6-8 inches",
            "Avoid eating 3 hours before bedtime",
            "Limit acidic/spicy/fatty foods",
            "Take antacids or PPIs as prescribed",
            "Report persistent symptoms despite treatment"
        ],
        'osteoarthritis': [
            "Apply heat/cold therapy for pain relief",
            "Maintain healthy weight to reduce joint stress",
            "Try low-impact exercises (swimming, cycling)",
            "Consider physical therapy",
            "Use assistive devices for painful joints"
        ],
        'rheumatoid arthritis': [
            "Take DMARDs/biologics as prescribed",
            "Practice joint protection techniques",
            "Maintain gentle range-of-motion exercises",
            "Monitor for medication side effects",
            "Report disease flares to rheumatologist"
        ],
        'depression': [
            "Maintain regular sleep schedule",
            "Engage in physical activity daily",
            "Practice mindfulness/meditation",
            "Continue prescribed medications",
            "Reach out to mental health professional if suicidal thoughts occur"
        ],
        'anxiety': [
            "Practice deep breathing exercises",
            "Limit caffeine and alcohol intake",
            "Establish consistent sleep routine",
            "Try progressive muscle relaxation",
            "Seek therapy for cognitive behavioral techniques"
        ],
        'migraine': [
            "Rest in quiet, dark room during attacks",
            "Take abortive medications at first sign",
            "Identify and avoid trigger factors",
            "Stay hydrated and maintain regular meals",
            "Consider preventive medications if frequent"
        ],
        'chronic kidney disease': [
            "Monitor blood pressure regularly",
            "Limit protein intake as directed",
            "Control blood sugar if diabetic",
            "Avoid NSAIDs and nephrotoxic substances",
            "Attend all nephrology appointments"
        ],
        'hypothyroidism': [
            "Take levothyroxine on empty stomach daily",
            "Wait 30-60 minutes before eating",
            "Get annual TSH level checks",
            "Report persistent fatigue or weight changes",
            "Avoid taking with calcium/iron supplements"
        ],
        'hypercholesterolemia': [
            "Follow heart-healthy diet low in saturated fats",
            "Take statins as prescribed",
            "Increase soluble fiber intake",
            "Exercise for 30 minutes most days",
            "Get regular lipid panel tests"
        ],
        'obesity': [
            "Aim for gradual weight loss (1-2 lbs/week)",
            "Increase daily physical activity",
            "Focus on portion control",
            "Keep food diary to track habits",
            "Consider nutritionist consultation"
        ],
        'iron deficiency anemia': [
            "Take iron supplements with vitamin C",
            "Increase iron-rich foods (red meat, spinach)",
            "Avoid taking with calcium or antacids",
            "Report black stools or abdominal pain",
            "Get follow-up blood tests"
        ],
        'diverticulitis': [
            "During flare-ups: liquid diet then low-fiber",
            "When healed: high-fiber diet",
            "Stay well hydrated",
            "Avoid nuts/seeds if prone to attacks",
            "Report fever or severe abdominal pain"
        ],
        'gout': [
            "Stay hydrated to flush uric acid",
            "Limit alcohol and high-purine foods",
            "Take prescribed medications during attacks",
            "Elevate and ice affected joint",
            "Maintain healthy weight"
        ]
    }

    # Default recommendations
    default_recommendations = [
        "Monitor symptoms closely",
        "Stay hydrated",
        "Get adequate rest",
        "Follow up with healthcare provider",
        "Seek emergency care for severe symptoms"
    ]

    # Get base recommendations
    recommendations = recommendations_map.get(disease.lower(), default_recommendations)
    
    # Add symptom-specific advice
    symptom_advice = {
        'fever': ["Monitor temperature regularly", "Use fever reducers if >101°F"],
        'chest pain': ["Seek emergency care for persistent chest pain"],
        'shortness of breath': ["Use pursed-lip breathing techniques", "Seek immediate care if severe"],
        'dizziness': ["Change positions slowly", "Avoid driving if severe"],
        'nausea': ["Try ginger tea or crackers", "Stay hydrated with small sips"]
    }
    
    # Add relevant symptom advice
    for symptom, advice in symptom_advice.items():
        if symptom in [s.lower() for s in symptoms]:
            recommendations.extend(advice)
    
    # Add severity-based advice
    severity = assess_severity(disease)
    if severity == 'severe':
        recommendations.insert(0, "⚠️ Seek medical attention immediately")
    elif severity == 'moderate':
        recommendations.insert(0, "Consult healthcare provider within 24-48 hours")
    
    # Remove duplicates while preserving order
    seen = set()
    return [x for x in recommendations if not (x in seen or seen.add(x))]

def calculate_confidence(symptoms):
    """Calculate confidence based on symptom specificity"""
    common_symptoms = {'headache', 'fever', 'fatigue'}
    specific_symptoms = {'jaundice', 'seizures', 'chest pain'}
    
    symptom_count = len(symptoms)
    specificity_score = sum(1 for s in symptoms if s in specific_symptoms)
    
    base_confidence = min(70 + (symptom_count * 5) + (specificity_score * 10), 95)
    return base_confidence

def assess_severity(disease):
    """Classify disease severity"""
    severity_map = {
        'common cold': 'mild',
        'flu': 'moderate',
        'pneumonia': 'severe',
        # Add more mappings
    }
    return severity_map.get(disease.lower(), 'moderate')

def about(request):
    """About page view"""
    return render(request, 'healthadvisor/about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Email subject and content
        subject = f'New Contact Form Submission from {name}'
        email_content = f"""
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """
        
        try:
            # Send email to yourself
            send_mail(
                subject,
                email_content,
                'g22.sarthak.sunil@gnkhalsa.edu.in',  # From email (uses DEFAULT_FROM_EMAIL from settings)
                ['g22.sarthak.sunil@gnkhalsa.edu.in'],  # To email (can be changed to any recipient)
                fail_silently=False,
            )
            
            # Optional: Send confirmation email to the user
            send_mail(
                'Thank you for contacting us',
                'We have received your message and will get back to you soon.\n\nYour message:\n' + message,
                'g22.sarthak.sunil@gnkhalsa.edu.in',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f'There was an error sending your message: {str(e)}')
        
        return redirect('contact')
    
    return render(request, 'healthadvisor/contact.html')