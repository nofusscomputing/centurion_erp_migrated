function openContentNavigationTab(evt, TabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("content-tab");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("content-navigation-tabs-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(TabName).style.display = "block";
    evt.currentTarget.className += " active";
}
