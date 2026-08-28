/*==========================================================
  MAIN.JS
  PART 1 — CORE WEBSITE INTERACTIONS
==========================================================*/

"use strict";

/*==========================================================
  DOM ELEMENTS
==========================================================*/

const navbar = document.getElementById("navbar");

const scrollTopBtn = document.getElementById("scrollTop");

const body = document.body;


/*==========================================================
  INITIALIZE WEBSITE
==========================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initializeWebsite();

});


function initializeWebsite(){

    updateNavbar();

    updateScrollButton();

    pageFadeIn();

}


/*==========================================================
  PAGE FADE IN
==========================================================*/

function pageFadeIn(){

    body.classList.add("loaded");

}


/*==========================================================
  STICKY NAVBAR
==========================================================*/

function updateNavbar(){

    if(!navbar) return;

    if(window.scrollY > 60){

        navbar.classList.add("navbar-scrolled");

    }

    else{

        navbar.classList.remove("navbar-scrolled");

    }

}


/*==========================================================
  SCROLL TO TOP BUTTON
==========================================================*/

function updateScrollButton(){

    if(!scrollTopBtn) return;

    if(window.scrollY > 500){

        scrollTopBtn.classList.add("show");

    }

    else{

        scrollTopBtn.classList.remove("show");

    }

}


if(scrollTopBtn){

    scrollTopBtn.addEventListener("click", () => {

        window.scrollTo({

            top:0,

            behavior:"smooth"

        });

    });

}


/*==========================================================
  WINDOW SCROLL EVENTS
==========================================================*/

window.addEventListener("scroll", () => {

    updateNavbar();

    updateScrollButton();

});


/*==========================================================
  WINDOW RESIZE
==========================================================*/

window.addEventListener("resize", () => {

    updateNavbar();

});

/*==========================================================
  PART 2 — SCROLL REVEAL ANIMATIONS
==========================================================*/

/*==========================================================
  ELEMENTS TO ANIMATE
==========================================================*/

const revealElements = document.querySelectorAll(

    ".section-header,\
     .feature-card,\
     .stat-card,\
     .pipeline-box,\
     .capability-card,\
     .cta-card,\
     .hero-card"

);


/*==========================================================
  INTERSECTION OBSERVER
==========================================================*/

const revealObserver = new IntersectionObserver(

    (entries) => {

        entries.forEach((entry) => {

            if(entry.isIntersecting){

                entry.target.classList.add("reveal-active");

                revealObserver.unobserve(entry.target);

            }

        });

    },

    {

        threshold:0.15,

        rootMargin:"0px 0px -50px 0px"

    }

);


/*==========================================================
  OBSERVE ELEMENTS
==========================================================*/

revealElements.forEach((element,index)=>{

    element.style.transitionDelay=`${index*0.08}s`;

    revealObserver.observe(element);

});

/*==========================================================
  PART 3 — ANIMATED COUNTERS
==========================================================*/

/*==========================================================
  COUNTER ELEMENTS
==========================================================*/

const counterElements = document.querySelectorAll(

    ".stat-card h2"

);

let counterAnimationPlayed = false;


/*==========================================================
  ANIMATE COUNTER
==========================================================*/

function animateCounter(element){

    const text = element.innerText;

    const numericValue = parseInt(

        text.replace(/\D/g,"")

    );

    if(isNaN(numericValue)) return;

    const suffix = text.replace(/[0-9]/g,"");

    const duration = 1800;

    const frameRate = 16;

    const totalFrames = duration / frameRate;

    const increment = numericValue / totalFrames;

    let current = 0;

    const timer = setInterval(()=>{

        current += increment;

        if(current >= numericValue){

            current = numericValue;

            clearInterval(timer);

        }

        element.innerText =

            Math.floor(current) + suffix;

    },frameRate);

}


/*==========================================================
  COUNTER OBSERVER
==========================================================*/

const counterObserver = new IntersectionObserver(

    (entries)=>{

        entries.forEach(entry=>{

            if(

                entry.isIntersecting &&

                !counterAnimationPlayed

            ){

                counterAnimationPlayed = true;

                counterElements.forEach(

                    animateCounter

                );

            }

        });

    },

    {

        threshold:0.45

    }

);


/*==========================================================
  START OBSERVER
==========================================================*/

const statisticsSection = document.querySelector(

    ".statistics"

);

if(statisticsSection){

    counterObserver.observe(

        statisticsSection

    );

}

/*==========================================================
  PART 4 — SMART NAVIGATION
==========================================================*/

/*==========================================================
  NAVIGATION LINKS
==========================================================*/

const navigationLinks = document.querySelectorAll(

    '.nav-links a[href^="#"]'

);

const pageSections = document.querySelectorAll(

    "main section[id]"

);


/*==========================================================
  SMOOTH SCROLL
==========================================================*/

navigationLinks.forEach((link)=>{

    link.addEventListener("click",(event)=>{

        event.preventDefault();

        const targetID =

            link.getAttribute("href");

        const targetSection =

            document.querySelector(targetID);

        if(!targetSection) return;

        const navbarHeight =

            navbar ? navbar.offsetHeight : 80;

        const targetPosition =

            targetSection.offsetTop - navbarHeight;

        window.scrollTo({

            top:targetPosition,

            behavior:"smooth"

        });

    });

});


/*==========================================================
  ACTIVE NAVIGATION LINK
==========================================================*/

function updateActiveNavigation(){

    let currentSection = "";

    pageSections.forEach((section)=>{

        const sectionTop =

            section.offsetTop - 120;

        const sectionHeight =

            section.offsetHeight;

        if(

            window.scrollY >= sectionTop &&

            window.scrollY < sectionTop + sectionHeight

        ){

            currentSection =

                section.getAttribute("id");

        }

    });

    navigationLinks.forEach((link)=>{

        link.classList.remove("active");

        if(

            link.getAttribute("href") ===

            "#" + currentSection

        ){

            link.classList.add("active");

        }

    });

}


/*==========================================================
  SCROLL THROTTLING
==========================================================*/

let scrollTicking = false;

window.addEventListener("scroll",()=>{

    if(scrollTicking) return;

    scrollTicking = true;

    requestAnimationFrame(()=>{

        updateNavbar();

        updateScrollButton();

        updateActiveNavigation();

        scrollTicking = false;

    });

});


/*==========================================================
  INITIAL ACTIVE LINK
==========================================================*/

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        updateActiveNavigation();

    }

);

/*==========================================================
  PART 5 — PREMIUM UI EFFECTS
==========================================================*/

/*==========================================================
  HERO CARD PARALLAX
==========================================================*/

const heroCard = document.querySelector(

    ".hero-card"

);

const heroSection = document.querySelector(

    ".hero"

);

if(heroCard && heroSection){

    heroSection.addEventListener(

        "mousemove",

        (event)=>{

            const rect =

                heroSection.getBoundingClientRect();

            const x =

                event.clientX - rect.left;

            const y =

                event.clientY - rect.top;

            const rotateY =

                ((x / rect.width) - 0.5) * 16;

            const rotateX =

                ((y / rect.height) - 0.5) * -16;

            heroCard.style.transform =

                `perspective(1200px)
                 rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 translateY(-8px)`;

        }

    );

    heroSection.addEventListener(

        "mouseleave",

        ()=>{

            heroCard.style.transform = "";

        }

    );

}


/*==========================================================
  BUTTON RIPPLE EFFECT
==========================================================*/

const rippleButtons = document.querySelectorAll(

    ".btn-primary, .btn-secondary, .btn-nav"

);

rippleButtons.forEach((button)=>{

    button.addEventListener(

        "click",

        function(event){

            const ripple =

                document.createElement("span");

            const rect =

                this.getBoundingClientRect();

            const size =

                Math.max(rect.width, rect.height);

            ripple.style.width =

                `${size}px`;

            ripple.style.height =

                `${size}px`;

            ripple.style.left =

                `${event.clientX - rect.left - size/2}px`;

            ripple.style.top =

                `${event.clientY - rect.top - size/2}px`;

            ripple.className =

                "ripple";

            this.appendChild(ripple);

            setTimeout(()=>{

                ripple.remove();

            },600);

        }

    );

});


/*==========================================================
  FLOATING HERO CARD
==========================================================*/

let floatAngle = 0;

function floatingAnimation(){

    if(heroCard){

        floatAngle += 0.015;

        heroCard.style.marginTop =

            `${Math.sin(floatAngle)*8}px`;

    }

    requestAnimationFrame(

        floatingAnimation

    );

}

floatingAnimation();


/*==========================================================
  GRADIENT PARALLAX
==========================================================*/

const gradients = document.querySelectorAll(

    ".gradient"

);

window.addEventListener(

    "mousemove",

    (event)=>{

        const x =

            event.clientX / window.innerWidth;

        const y =

            event.clientY / window.innerHeight;

        gradients.forEach(

            (gradient,index)=>{

                const speed =

                    (index+1)*12;

                gradient.style.transform =

                    `translate(
                        ${x*speed}px,
                        ${y*speed}px
                    )`;

            }

        );

    }

);


/*==========================================================
  CTA CARD GLOW
==========================================================*/

const ctaCard = document.querySelector(

    ".cta-card"

);

if(ctaCard){

    ctaCard.addEventListener(

        "mousemove",

        (event)=>{

            const rect =

                ctaCard.getBoundingClientRect();

            const x =

                event.clientX - rect.left;

            const y =

                event.clientY - rect.top;

            ctaCard.style.setProperty(

                "--mouse-x",

                `${x}px`

            );

            ctaCard.style.setProperty(

                "--mouse-y",

                `${y}px`

            );

        }

    );

}

/*==========================================================
  PART 6 — FINAL POLISH & PERFORMANCE
==========================================================*/

/*==========================================================
  REDUCED MOTION SUPPORT
==========================================================*/

const prefersReducedMotion =

    window.matchMedia(

        "(prefers-reduced-motion: reduce)"

    );

if(prefersReducedMotion.matches){

    document.documentElement.style.scrollBehavior =

        "auto";

}


/*==========================================================
  REMOVE RIPPLE AFTER ANIMATION
==========================================================*/

document.addEventListener(

    "animationend",

    (event)=>{

        if(

            event.target.classList.contains(

                "ripple"

            )

        ){

            event.target.remove();

        }

    }

);


/*==========================================================
  PREVENT IMAGE DRAGGING
==========================================================*/

document.querySelectorAll("img").forEach((image)=>{

    image.draggable = false;

});


/*==========================================================
  KEYBOARD ACCESSIBILITY
==========================================================*/

document.addEventListener(

    "keyup",

    (event)=>{

        if(

            event.key === "Escape"

        ){

            document.activeElement.blur();

        }

    }

);


/*==========================================================
  LAZY LOADING SUPPORT
==========================================================*/

document.querySelectorAll("img").forEach((image)=>{

    if(

        !image.hasAttribute("loading")

    ){

        image.setAttribute(

            "loading",

            "lazy"

        );

    }

});


/*==========================================================
  CONSOLE BRANDING
==========================================================*/

console.log(

    "%c🏎️ F1 AI Strategist",

    "color:#e10600;font-size:20px;font-weight:bold;"

);

console.log(

    "%cPremium Formula One Strategy Dashboard Loaded Successfully",

    "color:#ffffff;background:#111;padding:6px;border-radius:4px;"

);


/*==========================================================
  PAGE LOAD COMPLETE
==========================================================*/

window.addEventListener(

    "load",

    ()=>{

        document.body.classList.add(

            "page-loaded"

        );

    }

);


/*==========================================================
  END OF FILE
==========================================================*/