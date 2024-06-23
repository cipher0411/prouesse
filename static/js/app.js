    // Sticky Navbar
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });





    //inbox js
    document.addEventListener('DOMContentLoaded', function() {
        const inboxNumber = document.getElementById('inbox_number');

        // Function to update unread count and play notification sound
        function updateInboxCount() {
            fetch("{% url 'item:unread_messages_count' %}")
                .then(response => response.json())
                .then(data => {
                    const unreadCount = data.unread_count;
                    inboxNumber.textContent = unreadCount;
                    if (unreadCount > 0) {
                        playNotificationSound();
                    }
                })
                .catch(error => {
                    console.error('Error fetching unread count:', error);
                });
        }

        // Function to play notification sound
        function playNotificationSound() {
            // Replace with your notification sound file path
            const audio = new Audio("{% static 'sound/notification.wav' %}");
            audio.play();
        }

        // Update unread count on page load
        updateInboxCount();

        // Polling for unread count every 30 seconds
        setInterval(updateInboxCount, 30000); // 30 seconds interval
    });



    // // carousel slide show for heading

    // document.addEventListener('DOMContentLoaded', function() {
    //     const carousel = document.getElementById('carouselId');
    //     const carouselInstance = new bootstrap.Carousel(carousel, {
    //         interval: 5000, // Set the interval for automatic slide
    //         wrap: true // Enable wrap to make it loop seamlessly
    //     });

    //     // Move to the next slide when the last one is reached
    //     carousel.addEventListener('slid.bs.carousel', function() {
    //         if (carousel.querySelector('.carousel-item.active').nextElementSibling === null) {
    //             carouselInstance.to(0);
    //         }
    //     });

    //     // Move to the previous slide when the first one is reached
    //     carousel.addEventListener('slid.bs.carousel', function() {
    //         if (carousel.querySelector('.carousel-item.active').previousElementSibling === null) {
    //             carouselInstance.to(carousel.querySelectorAll('.carousel-item').length - 1);
    //         }
    //     });
    // });




    // Function to extract CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Update cart quantity in navbar
    function updateCartQuantity(quantity) {
        $('#cart_quantity').text(quantity);
    }

    // Add to Cart Button Clicked
    $(document).ready(function() {
        console.log('jQuery is loaded');

        $('.add-to-cart-btn').click(function() {
            console.log('Add to Cart button clicked');

            var item_id = $(this).val();
            console.log('Item ID:', item_id);

            // AJAX Post Request
            $.ajax({
                type: 'POST',
                url: '/items/' + item_id + '/add-to-cart/',
                data: {
                    'csrfmiddlewaretoken': getCookie('csrftoken') // Use the extracted CSRF token
                },
                dataType: 'json',
                success: function(response) {
                    console.log(response);

                    // Update Cart Quantity in Navbar
                    updateCartQuantity(response.cart_quantity);
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        });
    });







    $(document).ready(function() {
        $(".testi_slider").owlCarousel({
            items: 2, // Show 2 items in one slide
            loop: true,
            margin: 30,
            nav: true,
            autoplay: true,
            autoplayHoverPause: true,
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                }
            }
        });
    });



    //Calendly linking
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('scheduleMeetingButton').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior
        Calendly.initPopupWidget({
            url: 'https://calendly.com/estheradanma010/prouesse-fashion-meeting',
            color: '#0069ff',
            textColor: '#ffffff',
            branding: false
        });
    });
});