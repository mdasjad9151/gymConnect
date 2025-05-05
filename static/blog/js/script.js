
function getCsrfToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}

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
          "X-CSRFToken": getCsrfToken(),
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

  // comment section 

  document.querySelectorAll(".comment-button").forEach((button) => {
    button.addEventListener("click", function () {
      if (!isAuthenticated) {
        window.location.href = loginUrl;
        return;
      }

      let postId = this.dataset.postId;
      // console.log(postId)
      let commentSection = document.getElementById(`comments-${postId}`);
      let commentList = document.getElementById(`comments-list-${postId}`);
      // console.log(commentSection)

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
      // console.log(postId)
      let commentText = document.getElementById(`comment-text-${postId}`).value;
      let commentList = document.getElementById(`comments-list-${postId}`);
      console.log(commentText)

      fetch(`/posts/comment/add/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "Content-Type": "application/json",
        },
        
        body: JSON.stringify({ text: commentText }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
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
