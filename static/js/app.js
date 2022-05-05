window.onload = (event) => {
    initRipple();
    bodymovin.loadAnimation({
        container: document.getElementById("header_loader"),
        renderer: 'canvas',
        loop: true,
        autoplay: true,
        path: 'static/duck.json',
        rendererSettings: {
            clearCanvas: true,
        }
    });
}

function initRipple() {
    if (!document.querySelectorAll) return;
    const rippleHandlers = document.querySelectorAll('.ripple-handler');
    console.log(rippleHandlers);
    const redraw = function (el) {
        el.offsetTop + 1;
    };
    const isTouch = ('ontouchstart' in window);
    for (let i = 0; i < rippleHandlers.length; i++) {
        (function(rippleHandler) {
            function onRippleStart(e) {
                let clientY;
                let clientX;
                const rippleMask = rippleHandler.querySelector('.ripple-mask');
                if (!rippleMask) return;
                const rect = rippleMask.getBoundingClientRect();
                if (e.type === 'touchstart') {
                    clientX = e.targetTouches[0].clientX;
                    clientY = e.targetTouches[0].clientY;
                } else {
                    clientX = e.clientX;
                    clientY = e.clientY;
                }
                const rippleX = (clientX - rect.left) - rippleMask.offsetWidth / 2;
                const rippleY = (clientY - rect.top) - rippleMask.offsetHeight / 2;
                const ripple = rippleHandler.querySelector('.ripple');
                ripple.style.transition = 'none';
                redraw(ripple);
                ripple.style.transform = 'translate3d(' + rippleX + 'px, ' + rippleY + 'px, 0) scale3d(0.2, 0.2, 1)';
                ripple.style.opacity = "1";
                redraw(ripple);
                ripple.style.transform = 'translate3d(' + rippleX + 'px, ' + rippleY + 'px, 0) scale3d(1, 1, 1)';
                ripple.style.transition = '';

                function onRippleEnd(_) {
                    ripple.style.transitionDuration = 'var(--ripple-end-duration, .2s)';
                    ripple.style.opacity = "0";
                    if (isTouch) {
                        document.removeEventListener('touchend', onRippleEnd);
                        document.removeEventListener('touchcancel', onRippleEnd);
                    } else {
                        document.removeEventListener('mouseup', onRippleEnd);
                    }
                }
                if (isTouch) {
                    document.addEventListener('touchend', onRippleEnd);
                    document.addEventListener('touchcancel', onRippleEnd);
                } else {
                    document.addEventListener('mouseup', onRippleEnd);
                }
            }
            if (isTouch) {
                rippleHandler.removeEventListener('touchstart', onRippleStart);
                rippleHandler.addEventListener('touchstart', onRippleStart);
            } else {
                rippleHandler.removeEventListener('mousedown', onRippleStart);
                rippleHandler.addEventListener('mousedown', onRippleStart);
            }
        })(rippleHandlers[i]);
    }
}

function refreshPage() {
    setTimeout(() => {
        location.reload();
    }, 200);
}