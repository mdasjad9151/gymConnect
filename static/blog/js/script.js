document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".like-button").forEach((button) => {
    button.addEventListener("click", function () {
      if (!isAuthenticated) {
        window.location.href = loginUrl;
        return;
      }

      let postId = this.dataset.postId;
      let likeCount = document.getElementById(`like-count-${postId}`);

      fetch(`/posts/like/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": "{{ csrf_token }}",
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.textContent = data.liked ? "Unlike" : "Like";
          likeCount.textContent = data.like_count;
        });
    });
  });

  document.querySelectorAll(".comment-button").forEach((button) => {
    button.addEventListener("click", function () {
      if (!isAuthenticated) {
        window.location.href = loginUrl;
        return;
      }

      let postId = this.dataset.postId;
      let commentSection = document.getElementById(`comments-${postId}`);
      let commentList = document.getElementById(`comments-list-${postId}`);

      if (commentSection.classList.contains("hidden")) {
        commentSection.classList.remove("hidden");
        fetch(`/posts/comment/load/${postId}/`)
          .then((response) => response.json())
          .then((data) => {
            commentList.innerHTML = "";
            data.comments.forEach((comment) => {
              let commentHTML = `<p><strong>${comment.user}</strong>: ${comment.text} <small>(${comment.created_at})</small></p>`;
              commentList.innerHTML += commentHTML;
            });
          });
      } else {
        commentSection.classList.add("hidden");
      }
    });
  });

  document.querySelectorAll(".add-comment-button").forEach((button) => {
    button.addEventListener("click", function () {
      if (!isAuthenticated) {
        window.location.href = loginUrl;
        return;
      }

      let postId = this.dataset.postId;
      let commentText = document.getElementById(`comment-text-${postId}`).value;
      let commentList = document.getElementById(`comments-list-${postId}`);

      fetch(`/posts/comment/add/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": "{{ csrf_token }}",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `text=${encodeURIComponent(commentText)}`,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            let newComment = `<p><strong>${data.comment.user}</strong>: ${data.comment.text} <small>(${data.comment.created_at})</small></p>`;
            commentList.innerHTML += newComment;
            document.getElementById(`comment-text-${postId}`).value = "";
          } else {
            alert("Failed to add comment.");
          }
        });
    });
  });
});
