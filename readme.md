<h1>GymConnect: Gym Management System</h1>
GymConnect is a comprehensive gym management system that streamlines gym operations by enabling gym owners, trainers, and gym users to interact efficiently. The platform provides features like managing trainer requests, assigning trainers to gym users, and facilitating workout and diet plans.

<h2>Features</h2>
<h3>Gym Owner</h3>
Manage Trainers: View and handle trainer requests with options to accept or reject.
Assign Trainers: Assign trainers to gym users and track assignments.
User Management: View all users registered under the gym with assigned trainer details.
<h3>Trainer</h3>
Plan Management: Create and manage workout and diet plans for gym users.
Requests Dashboard: View gym-specific requests and gym details.
<h3>Gym User</h3>
Trainer Assignment: Get assigned to trainers based on gym owner approvals.
Workout and Diet Plans: Access personalized workout and diet plans created by trainers.
Technologies Used
<h3>Backend</h3>
Django
Authentication: Django's built-in authentication system
Frontend
CSS Framework: Tailwind CSS
JavaScript: For interactive UI components
Setup Instructions
Clone the Repository:

bash
Copy code
https://github.com/mdasjad9151/Chat-Connect.git
cd GymConnect
Create a Virtual Environment:

bash
Copy code
python -m venv venv  
source venv/bin/activate  # On Windows, use venv\Scripts\activate  
Install Dependencies:

bash
Copy code
pip install -r requirements.txt  
Configure the Database:

Update DATABASES in settings.py with your database credentials.
Run Migrations:

bash
Copy code
python manage.py makemigrations  
python manage.py migrate  
Load Static Files:

bash
Copy code
python manage.py collectstatic  
Run the Server:

bash
Copy code
python manage.py runserver  
Access the Application:
Open http://127.0.0.1:8000/ in your browser.

Usage
Admin Credentials
Default admin credentials can be created using:
bash
Copy code
python manage.py createsuperuser  
Gym Owner
Log in as a gym owner to manage users and trainers.
Trainer
Use the dashboard to manage requests and create plans.
Gym User
View assigned trainers and access workout/diet plans.
Contribution Guidelines
We welcome contributions to enhance GymConnect. Follow these steps to contribute:

Fork the repository.
Create a feature branch: git checkout -b feature-name.
Commit changes: git commit -m "Feature description".
Push to your branch: git push origin feature-name.
Submit a pull request.


