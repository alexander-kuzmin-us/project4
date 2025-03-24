document.addEventListener('DOMContentLoaded', function() {
    // Like/Unlike posts
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const isLiked = this.classList.contains('btn-danger');
            const action = isLiked ? 'unlike' : 'like';
            
            fetch(`/posts/${postId}/like`, {
                method: 'PUT',
                body: JSON.stringify({
                    action: action
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update like count
                    this.querySelector('.like-count').textContent = data.likes;
                    
                    // Toggle button style
                    if (action === 'like') {
                        this.classList.remove('btn-outline-danger');
                        this.classList.add('btn-danger');
                    } else {
                        this.classList.remove('btn-danger');
                        this.classList.add('btn-outline-danger');
                    }
                } else {
                    console.error('Error:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Edit post functionality
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const postCard = this.closest('.post');
            const postContent = postCard.querySelector('.post-content');
            const editArea = postCard.querySelector('.edit-area');
            const editContent = postCard.querySelector('.edit-content');
            
            // Show edit area, hide content
            postContent.style.display = 'none';
            editArea.style.display = 'block';
            
            // Focus the textarea
            editContent.focus();
        });
    });
    
    // Cancel edit
    document.querySelectorAll('.cancel-edit').forEach(button => {
        button.addEventListener('click', function() {
            const postCard = this.closest('.post');
            const postContent = postCard.querySelector('.post-content');
            const editArea = postCard.querySelector('.edit-area');
            
            // Hide edit area, show content
            postContent.style.display = 'block';
            editArea.style.display = 'none';
        });
    });
    
    // Save edit
    document.querySelectorAll('.save-edit').forEach(button => {
        button.addEventListener('click', function() {
            const postCard = this.closest('.post');
            const postId = postCard.dataset.postId;
            const postContent = postCard.querySelector('.post-content');
            const editArea = postCard.querySelector('.edit-area');
            const editContent = postCard.querySelector('.edit-content');
            
            fetch(`/posts/${postId}/edit`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: editContent.value
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update content
                    postContent.textContent = data.content;
                    
                    // Hide edit area, show content
                    postContent.style.display = 'block';
                    editArea.style.display = 'none';
                } else {
                    console.error('Error:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});