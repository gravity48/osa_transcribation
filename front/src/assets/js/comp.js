import $ from "jquery";

function event_list() {
    $('.accordion').click(function (e) {
        e.stopPropagation();
        e.preventDefault();
        if ($(this).siblings('.panel:first').height() === 0) {
            $(this).addClass('active');
            $(this).siblings('.panel:first').css({'max-height': $(this).siblings('.panel:first').prop('scrollHeight') + 'px'});
        } else {
            $(this).removeClass('active');
            $(this).siblings('.panel:first').css({'max-height': '0'});
        }
    });
    $(document).on('click', '.show-task-detail', function (e){
        e.stopPropagation();
        e.preventDefault();
        let detail_panel = $(this).parents('li:first').find('.task-detail-panel');
        if ($(detail_panel).height() === 0) {
            $(this).addClass('active');
            $(detail_panel).css({'max-height':$(detail_panel).prop('scrollHeight') + 'px' })
        } else {
            $(this).removeClass('active');
            $(detail_panel).css({'max-height': '0'});
        }
    });
    /*
    $('.block .vertical-menu li:not(:first,:nth-child(5))').click(function () {
        $('.block .vertical-menu li').removeClass('active');
        $(this).addClass('active');
    });

    $(document).on('click', '#settings-href', function (e){
       e.stopPropagation();
       e.preventDefault();
       $('.modal-settings').css({'display': 'flex'});
    });*/
    $(document).on('click', '.custom-select', function(e){
        e.stopPropagation();
        e.preventDefault();
        if ($(this).find('.custom-select-ico').hasClass('rotate')){
            $(this).find('.custom-select-ico').removeClass("rotate");
        }
        else{
            $(this).find('.custom-select-ico').addClass("rotate");
        }
        $(this).find('.custom-select-option').first().toggle();
    });
    $(document).on('click', '.custom-select-option ul li', function (e){
        e.stopPropagation();
        e.preventDefault();
        let value = $(e.currentTarget).attr('data-item');
        let name = $(e.currentTarget).text();
        let custom_select = $(e.currentTarget).parents('.custom-select');
        custom_select.find('input:first').val(value);
        custom_select.find('span').text(name);
        if (custom_select.find('.custom-select-ico').hasClass('rotate')){
            custom_select.find('.custom-select-ico').removeClass("rotate");
        }
        else{
            custom_select.find('.custom-select-ico').addClass("rotate");
        }
        custom_select.find('.custom-select-option').toggle();
    });
}

export default event_list;