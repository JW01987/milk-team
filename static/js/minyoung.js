const urlParams = new URLSearchParams(window.location.search);
let page = Number(urlParams.get('page'));
let limit = Number(urlParams.get('limit'));

// 초기 pmy.html 접속 시 쿼리문 전달이 없기 때문에 초기값 설정을 합니다.
if (page <= 0 && limit <= 0) {
  page = 1
  limit = 5
}

$(document).ready(function () {
  commentsListing();
});

async function commentsListing() {
  const response = await fetch(`/members/2/comments?page=${page}&limit=${limit}`);
  const data = await response.json();
  let { count, start_page, end_page, page_set, comments } = data

  $('#comment-list').empty()
  if (comments.length === 0) {
    $('#comment-list').append(`<p style="text-align: center; font-size: 20px;">아직 댓글이 없어요...</p>`)
  } else {
    comments.forEach((row) => {
      let { nick_name, comment, upload_time } = row
      let comment_html = `<div class="card">
                            <div class="card-body">
                              <blockquote class="blockquote mb-0">
                                <p>${comment}</p>
                                <footer class="blockquote-footer" id="footer">${nick_name} (${dateFormatter(upload_time)}) 
                                  <a href="#">수정</a>
                                  <a href="#">삭제</a>
                                </footer>
                              </blockquote>
                            </div>
                          </div>`
      $('#comment-list').append(comment_html)
    })
  }

  // pagination
  $('.pagination').empty()
  let total_page = Math.ceil(count / limit);

  if (page > page_set) {
    let previous = `<li class="page-item">
                      <a class="page-link" href="/minyoung?page=${start_page - page_set}&limit=${limit}" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                      </a>
                    </li>`
    $('.pagination').append(previous)
  }
  
  let page_list;
  for (let i = start_page; i <= end_page; i++) {
    let color 
    let url = `/minyoung?page=${i}&limit=${limit}`
    if (i > total_page) {
      break
    } else {
      if (page === i) {
        color = 'red'
      }
      page_list = `<li class="page-item"><a class="page-link" style="color: ${color};"href="${url}">${i}</a></li>`
    };
    $('.pagination').append(page_list)
  }
  
  if ((page <= total_page - (total_page % page_set)) && (total_page > page_set)) {
    let next = `<li class="page-item">
                  <a class="page-link" href="/minyoung?page=${start_page + page_set}&limit=${limit}" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                  </a>
                </li>`
    $('.pagination').append(next)
  }
}

async function posting() {
  let formData = new FormData();
  formData.append("nickname", inputChecker("닉네임", $("#nickname").val()));
  formData.append("password", inputChecker("비밀번호", $("#password").val()));
  formData.append("comment", inputChecker("코멘트", $("#comment").val()));

  const response = await fetch('/members/2/comments', { method: "POST", body: formData });
  const data = await response.json();
  alert(data['msg']);
  window.location.reload();
};

function inputChecker(target, content) {
  const trimString = content.trim()
  if (trimString.length === 0) {
    alert(`${target}을(를) 입력하세요.`);
    throw new Error(`${target}을(를) 입력하지 않았습니다.`);
  } else {
    return content
  };
};

function dateFormatter(dateString) {
  const inputDate = new Date(dateString);
  const year = inputDate.getFullYear();
  const month = String(inputDate.getMonth() + 1).padStart(2, "0");
  const day = String(inputDate.getDate()).padStart(2, "0");
  const hours = String(inputDate.getHours()).padStart(2, "0");
  const minutes = String(inputDate.getMinutes()).padStart(2, "0");
  const seconds = String(inputDate.getSeconds()).padStart(2, "0");
  const outputDateString = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  return outputDateString
};