$('.correct').change(function() {
    const $this = $(this),
        correct = $this.data("correct")
    console.log(correct)
    $.ajax('/correct/', {
        method: 'POST',
        data: {aid: correct}
    }).done(function (data) {

        if (data['aid'] != null) {
            const number = data['aid'];
            const span = $('span[data-aid="' + number + '"]');
            span.text(data['rating'])
        }
    })

    });