-# Threads-like Social Network

A responsive, Django-based social networking application with features similar to Threads/Twitter. This web application allows users to create accounts, make posts, follow other users, and engage with content through likes and comments.


## 📋 Features

- **User Authentication System**
  - Register new accounts
  - Secure login/logout functionality
  - Profile customization

- **Post Management**
  - Create text-based posts (up to 280 characters)
  - Edit your own posts with real-time updates
  - View posts chronologically

- **Social Interaction**
  - Follow/unfollow other users
  - Like/unlike posts with instant feedback
  - View personalized feed based on followed users

- **User Interface**
  - Responsive design for all device sizes
  - Intuitive navigation
  - Real-time notifications

- **Other Features**
  - Pagination (10 posts per page)
  - Profile pages with follower/following statistics
  - Asynchronous post updates without page refresh

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Django 3.0+
- Modern web browser

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/social-network.git
   cd social-network
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```bash
   python manage.py makemigrations network
   python manage.py migrate
   ```

5. Run the development server
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`

## 💻 Usage

1. **Create an Account**: Click "Register" to create a new account
2. **Create Posts**: Use the text box at the top of "All Posts" page
3. **Follow Users**: Visit user profiles and click "Follow"
4. **Interact with Posts**: Like posts or edit your own posts
5. **View Following Feed**: Click "Following" to see posts from users you follow

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Styling**: Bootstrap 4
- **Icons**: Font Awesome

## 📝 Project Structure

```
social-network/
├── network/                    # Main app directory
│   ├── static/                 # Static files
│   │   └── network/
│   │       ├── styles.css      # Custom CSS
│   │       └── threads.js      # JavaScript functionality
│   ├── templates/              # HTML templates
│   │   └── network/
│   │       ├── index.html      # Home page
│   │       ├── layout.html     # Base template
│   │       ├── following.html  # Following feed
│   │       ├── profile.html    # User profile
│   │       └── posts.html      # Post component
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   └── urls.py                 # URL routing
└── project4/                   # Project settings
    ├── settings.py             # Django settings
    └── urls.py                 # Project URL routing
```

## 🔄 API Endpoints

- `/posts/<post_id>/edit` - Update post content (PUT)
- `/posts/<post_id>/like` - Toggle post like status (PUT)
- `/profile/<username>` - View user profile (GET) or follow/unfollow (POST)

## 🧩 Models

- **User** - Extended Django User model with following relationship
- **Post** - Content, timestamp, and user relationship
- **Like** - Tracks post likes by users

## 🎯 Future Enhancements

- Comment system
- Image and video uploads
- Direct messaging
- Hashtag support
- Search functionality
- Advanced user profiles

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- [Alex Kuzmin](https://github.com/alexander-kuzmin-us)

---

Feel free to contribute to this project by submitting pull requests or reporting issues!
