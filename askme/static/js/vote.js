// console.log("HERE");

 // TODO: проверять поставил ли пользователь лайк на фронтенде

$('.js-vote').click(function(ev) {
    if ($(this).hasClass('disabled') == true)
        return;

    var ctx = new Map(); ;
    if ($(this).parent().parent().parent().hasClass('box-qst') == true)
        ctx['like'] = 'question';
    else if ($(this).parent().parent().parent().hasClass('box-answer') == true)
        ctx['like'] = 'answer';

    ev.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        id = $this.data('id');
        ctx['action'] = action;
        ctx['id'] = id;
    $.ajax('/vote/', {
        method: 'POST',
        data: ctx,
    }).done(function(data) {
        $('#like-rating-' + id).text(data.likes);
        console.log("DATA " + data);
    });
    console.log("HERE " + action + " " + id);
});
