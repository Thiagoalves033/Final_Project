$(document).ready(function() {
    $('.nav-link').on('click', function() {
        var activeTabId = $(this).attr('id');
        
        $('#activeTab').val(activeTabId);
        
        $(document).trigger('tabClicked', activeTabId);
    });
    
    $(document).on('tabClicked', function(event, activeTabId) {
        console.log(activeTabId);
    });
});
