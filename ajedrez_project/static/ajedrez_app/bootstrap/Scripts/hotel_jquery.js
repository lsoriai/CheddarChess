var jDesde = new Date();
var jHasta = new Date();
var manana = new Date();
var jNumHabitaciones = 0;
var jNumAdultos = 0;
var jNumNinos = 0;
var hoy = new Date();
var jNumNoches = 0;
var jVEdades=0;
var jZona = "";
var cadena="";
hoy = hoy.getDate();

var unavailableDates = [
    { start: '2015-09-11', end: '2015-09-15' },
    { start: '2015-09-15', end: '2015-09-23' },
    { start: '2015-10-01', end: '2015-10-07' }
];

window.addEventListener('load', inicio);
window.addEventListener('change', cambioNinos);
window.addEventListener('change', cambioHabitaciones);
window.addEventListener('change', cambioAdultos);
window.addEventListener('change', cambioDesde);
window.addEventListener('change', cambioHasta);
window.addEventListener('change', cambioValor);

function Autocompletar() {
    var ac = null;
    //ac = <%=listFilter %>;  
    $("#Country").autocomplete({
        source: ac
    });
}


function selectChanged(item) {
    alert("Item " + item.text + " (valor es: " + item.value + ")");
    var w = this.options[this.options.selectedIndex].value;
    alert(w);
}

function inicio() {
    var hoy = new Date();
    manana = new Date(hoy.getTime() + 24 * 60 * 60 * 1000);
    document.getElementById('desde').valueAsDate = hoy;
    document.getElementById('hasta').valueAsDate = manana;
    jDesde = hoy;
    jHasta = manana;
    jNumHabitaciones = 0;
    jNumAdultos = 0;
    jNumNinos = 0;
    jVEdades=0;
    setInterval(muestraReloj, 1000);
}

function cambioNinos()
{
    jNumNinos = document.getElementById("ninos").options.selectedIndex;
    if (jNumNinos >= 0)
    {
        //document.getElementById("capaoculta").style.display = "block";
        document.getElementById("valorNinos").innerHTML = jNumNinos;
        //document.getElementById("nNinos").innerHTML = "<font color='red' size='5'>" + jNumNinos + "</font>";
        document.getElementById("ppp").innerHTML = "<font color='red' size='5'>" + jNumNinos + "</font>";
        document.cookie = "cookieNinos=" + jNumNinos;
        // Autocompletar();
        return;
    }
    if (jNumNinos < 0) {
        //document.getElementById("capaoculta").style.display = "none";
        //document.getElementById("nNinos").innerHTML = "<font color='red' size='5'>0</font>";
        document.getElementById("valorNinos").innerHTML = jNumNinos;
        return;
    }
}

function cambioAdultos(num) {
    jNumAdultos = document.getElementById("adultos").options.selectedIndex;
    if (jNumAdultos > 0) {
        jNumAdultos = (jNumAdultos + 1);
        document.getElementById("valorAdul").innerHTML = "" + jNumAdultos + "";
        //document.getElementById("nAdul").innerHTML = "<font color='red' size='5'>" + jNumAdultos + "</font>";
        document.getElementById("ppp").innerHTML = "<font color='red' size='5'>" + jNumAdultos + "</font>";
        return;
    }
    if (jNumAdultos < 1) {
        document.getElementById("valorAdul").innerHTML = "1";
        document.getElementById("nAdul").innerHTML = "<font color='red' size='5'>1</font>";
        return;
    }
}
function cambioHabitaciones()
{
    jNumHabitaciones = document.getElementById("habitaciones").options.selectedIndex;
    if (jNumHabitaciones > 0)
    {
        jNumHabitaciones = (jNumHabitaciones + 1);
        document.getElementById("valorHab").innerHTML = "" + jNumHabitaciones + "";
        //document.getElementById("nHab").innerHTML = "<font color='red' size='5'>" + jNumHabitaciones + "</font>";
        document.getElementById("ppp").innerHTML = "<font color='red' size='5'>" + jNumHabitaciones + "</font>";
        return;
    }
    if (jNumHabitaciones < 1)
    {
        document.getElementById("valorHab").innerHTML = "1";
        document.getElementById("nHab").innerHTML = "<font color='red' size='5'>1</font>";
        return;
    }
}

function cambioValor() {
    //alert("entra en valor");
    //alert(jNumNinos);
    $('#NumNiños').val(jNumNinos);
    var x = document.cookie;
    //alert("cookie" + x);

}

function cambioDesde() {

    var hoy = new Date();
    var manana = new Date(hoy.getTime() + 24 * 60 * 60 * 1000);
    var diaElegido = document.getElementById('desde').valueAsDate;
    var hasta = document.getElementById('hasta').valueAsDate;
    if (diaElegido < hoy) {
        document.getElementById('desde').valueAsDate = hoy;
        jDesde = document.getElementById('desde').value;
        //alert("desde---------"+jDesde);
        return;
    }
    if (diaElegido >= hasta) {
        document.getElementById('desde').valueAsDate = diaElegido;
        manana = new Date(diaElegido.getTime() + 24 * 60 * 60 * 1000);
        document.getElementById('hasta').valueAsDate = manana;
        jDesde = document.getElementById('desde').value;
        //alert("desde---------" + jDesde);
        jHasta = document.getElementById('hasta').value;
        //alert("desde---------" + jHasta);
        return;
    }

    var posicion1 = document.getElementById("desde").value;
    if (posicion1 != "") {
        jDesde = posicion1;
    }
    return;
}

function cambioHasta() {

    var posicion = document.getElementById("desde").value;
    jDesde = posicion;
    var FechaHasta = document.getElementById("hasta").value;
    jHasta = FechaHasta;
    var hoy = new Date();

    if (jHasta <= jDesde) {
        document.getElementById('hasta').valueAsDate = manana;
        jHasta = manana;
        var cad = "<font color='blue' size='3'>" + "Estancia de 1 Noche</font>";
        document.getElementById("noches").innerHTML = cad;
        return;
    }
    var aFecha1 = jDesde.split('-');
    var aFecha2 = jHasta.split('-');
    var miFecha1 = new Date(aFecha1[0], aFecha1[1], aFecha1[2]);
    var miFecha2 = new Date(aFecha2[0], aFecha2[1], aFecha2[2]);
    var diferencia = miFecha2.getTime() - miFecha1.getTime();
    var dias = Math.floor(diferencia / (1000 * 60 * 60 * 24));
    var cad = "<font color='blue' size='3'>" + "Estancia de " + dias + " Noches</font>";
    document.getElementById("noches").innerHTML = cad;
    return;
}


function buscar() {
    alert("buscar");
}

function muestraReloj() {
    var fechaHora = new Date();
    var horas = fechaHora.getHours();
    var minutos = fechaHora.getMinutes();
    var segundos = fechaHora.getSeconds();

    if (horas < 10) { horas = '0' + horas; }
    if (minutos < 10) { minutos = '0' + minutos; }
    if (segundos < 10) { segundos = '0' + segundos; }

    document.getElementById("reloj").innerHTML = horas + ':' + minutos + ':' + segundos;
    return;
}


/*
$(document).ready(function () {
    $(".carousel").carousel({
        interval: 1000
    });
    $(".carousel").on("slid", function () {
        var to_slide;
        to_slide = $(".carousel-item.active").attr("data-slide-no");
        $(".myslide-target.active").removeClass("active");
        $(".cmyslide-indicators [data-slide-to=" + to_slide + "]").addClass("active");
    });
    $(".myslide-target").on("click", function () {
        $(this).preventDefault();
        $(".carousel").carousel(parseInt($(this).attr("data-slide-to")));
        $(".myslide-target.active").removeClass("active");
        $(this).addClass("active");
    });
});

*/