console.log("Namaste");

const url = window.location.host;
console.log(url);

const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const resultsBox = document.getElementById('results-box');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (post) => {
    $.ajax({
        type: 'POST',
        url: '/blog/post/search-ajax/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'post': post,
        },
        success: (res) => {
            console.log(res.data)
            console.log("success")
            const data = res.data
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                data.forEach(post=> {
                    console.log(post.slug);
                    resultsBox.innerHTML += `
                        <a href="/blog/${post.slug}/" class="item">
                            <div class="row" mt-2 mb-3 p-3>
                                <div class="col-2">
                                    <img src=${post.cover}>
                                </div>
                                <div class="col-10 ajax-post-title">
                                    <h5>${post.title}</h5>
                                </div>
                            </div>
                        </a>
                    `
                })
            } else {
                if (searchInput.value.length > 0) {
                    resultsBox.innerHTML = `<b>${data}</b>`
                } else {
                    resultsBox.classList.add('none')
                }
            }
        },
        error: (err) => {
            console.log(err);
            console.log("err")
        }
    })
}

searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)
    if (resultsBox.classList.contains('none')){
        resultsBox.classList.remove('none')
    }

    sendSearchData(e.target.value)
})