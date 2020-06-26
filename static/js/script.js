
$(".distribute-table-link").click(function (ev) {
    let link = $(ev.currentTarget);
    let modalId = link.attr('data-target');
    $(modalId).find(".modal-body").load(link.attr('href'));
});

$(".comment").blur(function (ev) {
    let comment = $(ev.currentTarget);
    let position_id = comment.attr('id').split('_')[1];
    let form = $(`#form_position_${position_id}`);
    console.log(form)
    //let csrfmiddlewaretoken =
    $.post( `/position/${position_id}/comment/`, $(form).serialize())
});
