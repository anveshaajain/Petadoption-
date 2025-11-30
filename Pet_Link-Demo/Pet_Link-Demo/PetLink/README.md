# 🐾 PetLink - Pet Adoption and Management System

PetLink is a modern, full-stack Pet Adoption and Management System built using Python Flask and SQLite. It connects loving families with pets in need of homes through an intuitive and responsive web platform.

GitHub Repository: [https://github.com/anveshaajain/PetLink.git](https://github.com/anveshaajain/PetLink.git)

---

## ✨ Key Features

### 👤 For Pet Adopters

#### Account & Profile
- **User Registration & Login:** Secure account creation with personal details
- **Profile Management:** View and update your profile information (name, contact, address, password)
- **Profile Deletion:** Safely delete your account with password confirmation
- **Adoption History:** Track all your adoption requests with status updates

#### Pet Discovery
- **Advanced Search:** Live search bar with real-time suggestions as you type
- **Status Filtering:** Filter pets by adoption status (Available, Adopted, Pending, All)
- **Category Browsing:** Explore pets by category (Dogs, Cats, Birds, Others)
- **Pet Detail Pages:** View comprehensive pet information including:
  - Large pet images
  - Health status and medical history (collapsible)
  - Owner contact information (optional reveal)
  - Like counts and adoption status

#### Pet Interaction
- **Like Pets:** Show your interest by liking pets (heart icon with count)
- **One-Click Adoption Requests:** Request adoption with a single click
  - Automatic request submission
  - Visual feedback (button turns green on success)
  - Success message: "Request sent successfully to owner"
- **Request Tracking:** Monitor request status (Pending, Approved, Rejected) in your profile

#### Community Features
- **Care Tips Blog:** Read and share pet care articles
- **Comments:** Engage with care tip posts by leaving comments
- **Community Learning:** Learn from other pet owners' experiences

### 🏥 For Pet Owners/Admins

#### Dashboard & Analytics
- **Comprehensive Dashboard:** Full-featured interface with real-time statistics
- **Analytics Overview:**
  - Total pets, available pets, adopted pets
  - Total requests with breakdown (pending, approved, rejected)
  - Adoption rate percentage
- **Top Pets Section:** See which pets receive the most adoption requests
- **Recent Activity Timeline:** Visual timeline of recent requests and pet additions
- **Category Distribution:** View pets grouped by category

#### Pet Management
- **Add Pets:** Create new pet listings with complete information
- **Edit Pets:** Update pet details, status, and information
- **Delete Pets:** Remove pets from the system
- **Status Management:** Update adoption status (Available, Adopted)

#### Request Management
- **Review Requests:** View all adoption requests for your pets
- **Approve/Reject:** Handle requests with one-click actions
- **Request Details:** See user information, messages, and contact details
- **Automatic Status Updates:** Pet status updates automatically when requests are approved

### 🎨 User Experience

#### Navigation & Search
- **Smart Search Bar:** 
  - Live search with dropdown results
  - Status filter dropdown
  - Click to navigate to pet details
  - Shows pet images and key information in results
- **Intuitive Navigation:** Easy access to all features from the header
- **Breadcrumbs:** Clear navigation paths throughout the app

#### Design & Interface
- **Responsive Design:** Fully functional on desktops, tablets, and mobiles
- **Dark/Light Mode:** Toggle themes with preferences saved automatically
- **Modern Styling:** Clean, professional interface with smooth animations
- **Bootstrap-Style Alerts:** 
  - Success (green)
  - Error/Danger (red)
  - Warning (yellow)
  - Info (blue)
  - Dismissible with close buttons
- **Compact UI:** Smaller, well-aligned buttons for better space utilization
- **Visual Feedback:** 
  - Loading states
  - Success indicators
  - Error messages
  - Interactive hover effects

#### Interactive Features
- **Real-Time Updates:** Like counts and request statuses update without page reload
- **AJAX Requests:** Smooth, asynchronous operations
- **Modal Dialogs:** For confirmations and detailed forms
- **Collapsible Sections:** Medical history and owner contact information

### 📚 Care Tips Section

- **Blog-Style Posts:** Community-driven pet care articles
- **Post Creation:** Users can share their pet care knowledge
- **Comments System:** 
  - Leave comments on care tip posts
  - View comment counts
  - Real-time comment addition
  - Author information and timestamps
- **Post Details:** Full post view with all comments
- **Community Engagement:** Learn from experienced pet owners

### 📦 Database & Security

#### Database Schema
- **Users Table:** User accounts with profile information
- **Owners Table:** Pet owner/admin accounts
- **Categories Table:** Pet categories (Dogs, Cats, Birds, Others)
- **Pets Table:** Complete pet information with images
- **Adoption Requests Table:** Request tracking with status
- **Pet Likes Table:** User likes for pets
- **Care Posts Table:** Community care tip articles
- **Care Comments Table:** Comments on care posts

#### Security Features
- **Password Hashing:** SHA-256 encryption for all passwords
- **Session-Based Authentication:** Secure user sessions
- **SQL Injection Prevention:** Parameterized queries throughout
- **Input Validation:** Server-side validation for all inputs
- **CSRF Protection:** Session-based request validation
- **Secure Data Handling:** Safe storage and retrieval of sensitive information

#### Automatic Setup
- **Auto-Initialization:** Database and tables created automatically on first run
- **Preloaded Data:** Sample pets and categories included
- **Default Admin:** Pre-configured owner account for testing

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the Project**
```bash
git clone https://github.com/anveshaajain/PetLink.git
cd PetLink
```

2. **Install Dependencies**
```bash
pip install flask
```

3. **Run the Application**
```bash
python app.py
```

4. **Open in Browser**
- Main app: [http://localhost:5000](http://localhost:5000)
- Owner login: [http://localhost:5000/owner-login](http://localhost:5000/owner-login)

### Demo Credentials

**Owner/Admin:**
- Email: `admin@petlink.com`
- Password: `admin123`

**User Account:**
- Create a new account via the registration page

---

## 📱 How to Use

### For Pet Adopters

1. **Register** – Create an account with your personal details
2. **Browse Pets** – Use the search bar or browse by category
3. **View Details** – Click on any pet to see full information
4. **Like Pets** – Show interest by clicking the heart icon
5. **Request Adoption** – Click "Adopt" button to send a request (one-click, no form needed)
6. **Track Requests** – Check your profile for request status updates
7. **Update Profile** – Edit your information anytime from the profile page
8. **Share Care Tips** – Post articles and comment on others' posts

### For Pet Owners/Admins

1. **Login** – Access the dashboard via owner login
2. **View Analytics** – Check statistics, top pets, and recent activity
3. **Add Pets** – Create new pet listings with complete details
4. **Manage Pets** – Edit or delete existing pets
5. **Review Requests** – See all adoption requests for your pets
6. **Approve/Reject** – Handle requests with one-click actions
7. **Monitor Activity** – Track adoption trends and popular pets

---

## 🗂 Project Structure

```
PetLink/
├── app.py                    # Main Flask application
├── petlink.db                # SQLite database (auto-created)
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── base.html            # Base template with styling and navigation
│   ├── index.html           # Home page with featured pets
│   ├── login.html           # User login page
│   ├── register.html         # User registration
│   ├── owner_login.html     # Owner/admin login
│   ├── profile.html         # User profile with editable fields
│   ├── adopt.html           # Pet browsing with search and filters
│   ├── pet_detail.html      # Individual pet detail page
│   ├── owner_dashboard.html # Owner dashboard with analytics
│   ├── care_list.html       # Care tips blog listing
│   ├── care_detail.html     # Individual care post with comments
│   ├── care_new.html        # Create new care tip post
│   ├── _search_component.html # Search bar component
│   ├── 404.html             # Error page
│   └── 500.html             # Error page
└── README.md                # This file
```

---

## 🔧 Technical Details

### Backend
- **Framework:** Flask (Python web framework)
- **Database:** SQLite (lightweight, file-based)
- **Authentication:** Session-based with password hashing
- **API Endpoints:** RESTful JSON APIs for AJAX operations

### Frontend
- **HTML5:** Semantic markup
- **CSS3:** Custom CSS with CSS variables for theming
- **JavaScript:** Vanilla JS for interactivity
- **Icons:** Font Awesome 6.0
- **Responsive Design:** Mobile-first approach

### Database Schema
- **Users:** id, name, email, password, contact, address, created_at
- **Owners:** id, name, email, password, contact, created_at
- **Categories:** id, name
- **Pets:** id, name, category_id, breed, age, health_details, medical_details, adoption_status, image_url, owner_id, created_at
- **Adoption Requests:** id, user_id, pet_id, status, message, created_at
- **Pet Likes:** id, pet_id, user_id, created_at
- **Care Posts:** id, user_id, title, content, created_at
- **Care Comments:** id, post_id, user_id, content, created_at

### Key Routes

#### Public Routes
- `GET /` - Home page
- `GET /adopt` - Browse pets
- `GET /pet/<id>` - Pet detail page
- `GET /care` - Care tips listing
- `GET /care/<id>` - Care post detail
- `GET /search_pets` - Search API endpoint

#### User Routes
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET/POST /profile` - Profile management
- `POST /request-adoption/<id>` - Submit adoption request
- `POST /like-pet/<id>` - Like/unlike a pet
- `POST /care/new` - Create care tip post
- `POST /care/<id>/comment` - Add comment to post
- `POST /delete-profile` - Delete user account

#### Owner Routes
- `GET/POST /owner-login` - Owner login
- `GET /owner-dashboard` - Dashboard with analytics
- `GET /owner-dashboard/analytics` - Analytics API
- `POST /add-pet` - Add new pet
- `POST /update-pet/<id>` - Update pet
- `POST /delete-pet/<id>` - Delete pet
- `POST /update-request-status/<id>` - Approve/reject request

---

## 🎯 Features in Detail

### Search Functionality
- **Live Search:** Real-time results as you type
- **Status Filter:** Filter by Available, Adopted, Pending, or All
- **Dropdown Results:** Shows pet images, names, and key details
- **Quick Navigation:** Click any result to view full details

### Pet Liking System
- **One-Click Like:** Simple heart button to show interest
- **Like Counts:** See how many users like each pet
- **Visual Feedback:** Liked pets show red heart
- **Real-Time Updates:** Counts update without page reload

### Adoption Request Flow
- **One-Click Request:** No form needed, instant submission
- **Visual Feedback:** Button turns green on success
- **Success Message:** "Request sent successfully to owner"
- **Duplicate Prevention:** Button disabled after successful request
- **Default Message:** Automatic message if none provided

### Owner Analytics
- **Statistics Dashboard:** 
  - Total pets count
  - Available vs adopted breakdown
  - Total requests with status breakdown
  - Adoption rate percentage
- **Top Pets:** Ranked by number of requests
- **Activity Timeline:** Visual history of recent actions
- **Category Insights:** Distribution of pets by category

### Care Tips Community
- **Blog Posts:** Users can share pet care knowledge
- **Comments:** Engage in discussions on posts
- **Author Attribution:** See who posted and when
- **Rich Content:** Full text posts with formatting

---

## 🔒 Security Features

- **Password Hashing:** SHA-256 encryption for all passwords
- **Session Management:** Secure session-based authentication
- **SQL Injection Prevention:** Parameterized queries throughout
- **Input Validation:** Server-side validation for all inputs
- **XSS Protection:** Proper escaping of user-generated content
- **CSRF Protection:** Session-based request validation
- **Secure Data Handling:** Safe storage and retrieval

---

## 🚀 Future Improvements

Potential enhancements for future versions:

- Email notifications for adoption requests
- Advanced search filters (age, breed, size)
- Pet photo upload functionality
- Adoption contract generation
- Payment integration for adoption fees
- Mobile app version (iOS/Android)
- Social media integration
- Push notifications
- Pet health records management
- Vet appointment scheduling
- Multi-language support
- Admin panel for system management

---

## 🐛 Troubleshooting

### Common Issues

**Port Conflicts:**
- Change Flask port in `app.py` (line 1114): `app.run(debug=True, host='0.0.0.0', port=5000)`

**Database Issues:**
- Delete `petlink.db` and restart the application
- Database will be recreated automatically

**Module Not Found:**
- Ensure Flask is installed: `pip install flask`
- Check Python version: `python --version` (requires 3.7+)

**JSON Serialization Errors:**
- Ensure all database queries convert Row objects to dictionaries
- Check that all API endpoints return proper JSON

**Button Not Working:**
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure you're logged in for user-specific features

---

## 🤝 Contributing

Contributions are welcome! You can:

- Report bugs via GitHub Issues
- Suggest new features
- Improve documentation
- Enhance UI/UX
- Add new functionality
- Optimize performance
- Improve security

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👥 Credits

Developed with ❤️ for pet lovers everywhere.

**Technologies Used:**
- Flask - Web framework
- SQLite - Database
- HTML5/CSS3/JavaScript - Frontend
- Font Awesome - Icons

---

## 📞 Support

For issues, questions, or contributions, please use the GitHub repository's issue tracker.

---

**Happy Pet Adopting! 🐾**
