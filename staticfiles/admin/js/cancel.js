<<<<<<< HEAD
'use strict';
{
    // Call function fn when the DOM is loaded and ready. If it is already
    // loaded, call the function now.
    // http://youmightnotneedjquery.com/#ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(function() {
        function handleClick(event) {
            event.preventDefault();
            const params = new URLSearchParams(window.location.search);
            if (params.has('_popup')) {
                window.close(); // Close the popup.
            } else {
                window.history.back(); // Otherwise, go back.
            }
        }

        document.querySelectorAll('.cancel-link').forEach(function(el) {
            el.addEventListener('click', handleClick);
        });
    });
}
=======
(function($) {
    'use strict';

    $(document).ready(function() {
        $('.cancel-link').click(function(e) {
            e.preventDefault();
            const parentWindow = window.parent;
            if (parentWindow && typeof(parentWindow.dismissRelatedObjectModal) === 'function' && parentWindow !== window) {
                parentWindow.dismissRelatedObjectModal();
            } else {
                // fallback to default behavior
                window.history.back();
            }
            return false;
        });
    });
})(django.jQuery);
>>>>>>> c4b91c71838ddf795a27b0a664db174292421dcf
