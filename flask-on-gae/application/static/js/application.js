// Some general UI pack related JS
// Extend JS String with repeat method
String.prototype.repeat = function(num) {
    return new Array(num + 1).join(this);
};

(function($) {


  $(function() {
  
    // Custom Select
    $("select[name='duration']").selectpicker({style: 'btn-primary', menuStyle: 'dropdown-inverse'});

    
  });
  
})(jQuery);