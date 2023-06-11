window.onload = (_) => {
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

const appHeight = () => {
    const doc = document.documentElement
    doc.style.setProperty('--app-height', `${window.innerHeight}px`)
}
window.addEventListener('resize', appHeight)
appHeight()

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

function openItem(element) {
    setTimeout(() => {
        window.scrollTo(0, 1);
        const data = JSON.parse(element.getElementsByClassName('data')[0].innerHTML);
        const dialog = document.getElementsByClassName('dialog')[0];
        dialog.style.display = '';
        setTimeout(() => {
            dialog.style.opacity = '1';
            dialog.style.backdropFilter = 'blur(5px)';
        }, 25);
        let textMessage = "<p><b>Banned User</b><br>ID: " + data.ID + "</p>";
        textMessage += "<p><b>Operator</b><br>ID: " + data.Operator.ID + "<br>"
        textMessage += "Name: <a target='_blank' href='https://t.me/" + data.Operator.Username.substring(1) + "'>" + data.Operator.Name + "</a></p>";
        document.getElementById('dialog_data').innerHTML = textMessage;
    }, 100);
}

function closeDialog() {
    const dialog = document.getElementsByClassName('dialog')[0];
    dialog.style.opacity = '0';
    dialog.style.backdropFilter = 'blur(0px)';
    setTimeout(() => {
        dialog.style.display = 'none';
    }, 250);
}
