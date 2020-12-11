console.log("HERE");

$('.js-correct').click(function(ev) {

    var ctx = new Map();
    ev.preventDefault();
    var $this = $(this),
        aid = $this.data('id'),
        qid = $('.box-qst').first().data('id');

    ctx['aid'] = aid;
    ctx['qid'] = qid;
    $.ajax('/correct/', {
        method: 'POST',
        data: ctx,
    }).done(function(data) {
      $this.prop('checked', data.is_correct)
        console.log("DATA " + data);
    });
    console.log("HERE " + aid + ", " + qid);
});
