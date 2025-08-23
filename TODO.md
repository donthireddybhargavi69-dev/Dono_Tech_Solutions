# TODO: Make Register Form Fields Mandatory

## Steps to Complete:

1. [ ] Update StudentRegistrationForm in forms.py to make all fields required
2. [ ] Update Student model in models.py to remove blank/null defaults from required fields
3. [ ] Update register.html template to add HTML5 required attributes
4. [ ] Run database migrations
5. [ ] Test the registration functionality

## Fields to Make Mandatory:
- username (already required)
- email
- phone_number
- gender
- date_of_birth
- college
- year_semester (already required)
- department
- courses_registered
- mentor

## Fields to Keep Optional:
- profile_image (for better user experience)
- password (already has required attribute)

## Current Status:
Starting implementation...
