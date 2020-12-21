$('.js-vote').click(function (event) {
    event.preventDefault()
    const $this = $(this),
        action = $this.data("action"),
        qid = $this.data("qid"),
        aid = $this.data("aid");
    let url = ""
    let data = {}
        if (aid == null) {
            url = "/vote/"
            data = {
                action: action,
                qid: qid,
            }
        } else {
            url = "/vote_answer/"
            data = {
                action: action,
                aid: aid,
            }
        }
    $.ajax(url, {
            method: 'POST',
            data: data
        }).done(function (data) {
            if (data['error'] != null) {
                alert(data['error'])
            }
            if (data['qid'] != null) {
                const number = data['qid'];
                const span = $('span[data-qid="' + number + '"]');
                span.text(data['rating'])
            }

            if (data['aid'] != null) {
                const number = data['aid'];
                const span = $('span[data-aid="' + number + '"]');
                span.text(data['rating'])
            }
        })
    }
)
