const app=new Vue({
    el:'#app',
    delimiters:["{","}"],
    data:{
        // csrftoken: Cookies.get('csrftoken'), // Using JS Cookies library
        // headers: {'X-CSRFTOKEN': this.csrftoken},
        padre: null,
        disenos:[],
        disenosHijos:[],
        disenosHijosAgregados:[],
        unidadesHijas:[],
        subUnidadesHijas:[],
        unidadesHijasAgregadas:[],
        subUnidadesHijasAgregadas:[],
        // objEspecificosHijos:[],
        areas:[],
        especialidades:[],
        objEspecificos:[],
        unidades:[],
        subUnidades:[],
        recursos:[],
        referencias:[],
        lecturas:[],
        codeTipo:null,
        codeEsp:null,
        tipoEvento:[{id:1,nombre:"Programa"},{id:2,nombre:"Diplomado"},{id:3,nombre:"Curso"},{id:4,nombre:"Conferencia"},{id:5,nombre:"Charla"},{id:6,nombre:"Seminario"},{id:7,nombre:"Webinario"}],
        tiposRecursos:["Equipos","Materiales Didácticos","Software","Hardware","Aula/Laboratorio"],
        modalidades:["Presencial","Semi-Presencial","Virtual"],
        tipoCertificado:["Aprobación","Participación"],
        //obj Especifico
        crearObjEspecifico:"",
        newObjEspecifico:"",
        formActualizarObj:false,
        indexUpdateObj:-1,
        //unidad
        formActualizarUni:false,
        numUnidadUpdate:null,
        detalleUnidad:"",
        horasPresencialesUni:null,
        horasAutonomasUni:null,
        horasTotalUni:null,
        objetivoUni:"",
        newdetalleUnidad:"",
        newhorasPresencialesUni:null,
        newhorasAutonomasUni:null,
        newhorasTotalUni:null,
        newobjetivoUni:"",
        //subUnidad
        formActualizarSubUni:false,
        indexSubUnidad:-1,
        detalleSubUnidad:"",
        horasPresencialesSubUni:null,
        horasAutonomasSubUni:null,
        horasTotalSubUni:null,
        newnumSubUnidad:"",
        newhorasPresencialesSubUni:null,
        newhorasAutonomasSubUni:null,
        newhorasTotalSubUni:null,
        //recursos
        formActualizarRecurso:false,
        indexUpdateRecurso:null,
        tipoRecurso:"",
        descripcionRecurso:"",
        newtipoRecurso:"",
        newdescripcionRecurso:"",
        //referencias
        formActualizarReferencia:false,
        indexUpdateReferencia:null,
        tipoReferencia:"Libro",
        tituloReferencia:"",
        autorReferencia:"",
        publicacionReferencia:"",
        editorialReferencia:"",
        paisReferencia:"",
        consultaReferencia:"",
        sitioReferencia:"",
        enlaceReferencia:"",
        descripcionReferencia:"",
        newtipoReferencia:"",
        newtituloReferencia:"",
        newautorReferencia:"",
        newpublicacionReferencia:"",
        neweditorialReferencia:"",
        newpaisReferencia:"",
        newconsultaReferencia:"",
        newsitioReferencia:"",
        newenlaceReferencia:"",
        newdescripcionReferencia:"",
        //lecturas
        formActualizarLectura:false,
        indexUpdateLectura:null,
        tipoLectura:"Libro",
        tituloLectura:"",
        autorLectura:"",
        publicacionLectura:null,
        editorialLectura:"",
        paisLectura:"",
        consultaLectura:"",
        sitioLectura:"",
        enlaceLectura:"",
        descripcionLectura:"",
        newtipoLectura:"",
        newtituloLectura:"",
        newautorLectura:"",
        newpublicacionLectura:null,
        neweditorialLectura:"",
        newpaisLectura:"",
        newconsultaLectura:"",
        newsitioLectura:"",
        newenlaceLectura:"",
        newdescripcionLectura:"",
       //modelos
        newDesign:{
            "es_padre": false,
            "codigo": "",
            "nombre": "",
            "version": null,
            "cod_programa": "",
            "modalidad": "",
            "tipo_certificado": "",
            "estado": "En proceso",
            "requisitos_facilitador": "",
            "horas_presenciales": null,
            "horas_autonomas": null,
            "horas_totales": null,
            "justificacion": "",
            "objetivo": "",
            "dirigido_participante": "",
            "indispensable_participante": "",
            "recomendables_participante": "",
            "metodologia1": false,
            "metodologia2": false,
            "metodologia3": false,
            "metodologia4": false,
            "metodologia5": false,
            "metodologia6": false,
            "metodologia7": false,
            "metodologia8": false,
            "area": null,
            "especialidad": null,
            "tipo_evento": null
        },
        designtemp:{},
        objetivo_sub:{},
        tempuni:{},
        ultimoIdDiseno:null,
        showModal: false  
    },
    mounted: function() {
        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
        this.getDisenos();
        this.getAreas();
        this.getEspecialidades();
        this.getUnidadesHijas();
        this.getSubUnidadesHijas();
        // this.getObjetivosEspecificos();  NO PARECE SER NECESARIO OBTENER LOS OBJETIVOS ESPECIFICOS DE LOS HIJOS
        //this.getTipoEvento();             POR AHORA FUNCIONARA CON VALORES QUEMADOS, DE LO CONTRARIO: DESCOMENTAR Y VACIAR LA LISTA TIPO EVENTO PARA USAR LA API
    },

    methods:{
        getDisenosHijos: function(){
            axios.get('/api/disenoHijo/').then((response)=>{
                this.disenosHijos=response.data;
            }).catch((err)=>{
                console.log(err);
            })
        },
        agregarHijo: function(index){
            this.disenosHijosAgregados.push(this.disenosHijos[index]);
            this.addUnidadesHijas(this.disenosHijos[index]);
            this.addSubUnidadesHijas(this.disenosHijos[index]);
            this.disenosHijos.splice(index,1);
        },
        removerHijo: function(index){
            this.disenosHijos.push(this.disenosHijosAgregados[index]);
            this.removerUnidadesHijas(this.disenosHijosAgregados[index]);
            this.removerSubUnidadesHijas(this.disenosHijosAgregados[index]);
            this.disenosHijosAgregados.splice(index,1);
        },
        guardarEstado: function(tipo){
            if (tipo==="Programa" || tipo==="Diplomado"){
                this.padre = true;
                this.newDesign.es_padre = true;
                this.getDisenosHijos();
            }
            else{
                this.padre = false;
                this.newDesign.es_padre = false;
            }
            this.codeTipo = tipo[0]+tipo[1].toUpperCase();
        },
        getDisenos: function(){
            axios.get('/academico/api/design/').then((response)=>{
                this.disenos = response.data;
            }).catch((err)=>{
                console.log(err)
            });
        },
        getUnidadesHijas: function(){
            axios.get('/academico/api/unidad/').then((response)=>{
                this.unidadesHijas=response.data;
            }).catch((err)=>{
                console.log(err)
            });
            
        },
        getSubUnidadesHijas: function(){
            axios.get('/academico/api/subUnidad/').then((response)=>{
                this.subUnidadesHijas=response.data;
            }).catch((err)=>{
                console.log(err)
            });
            
        },
        addUnidadesHijas: function(diseno){
                for (var unidad of this.unidadesHijas){
                    if(diseno.id == unidad.design){
                        this.unidadesHijasAgregadas.push(unidad);
                    }
                }
        },
        addSubUnidadesHijas: function(diseno){
                for (var subUnidad of this.subUnidadesHijas){
                    if(diseno.id == subUnidad.design){
                        this.subUnidadesHijasAgregadas.push(subUnidad);
                    }
                }
        },
        removerUnidadesHijas: function(diseno){
            for (var unidad of this.unidadesHijas){
                console.log(unidad.design);
                if(diseno.id == unidad.design){
                    this.unidadesHijasAgregadas.splice(this.unidadesHijasAgregadas.indexOf(unidad),1)
                }
            }
        },
        removerSubUnidadesHijas: function(diseno){
            for (var subUnidad of this.subUnidadesHijas){
                if(diseno.id == subUnidad.design){
                    this.subUnidadesHijasAgregadas.splice(this.subUnidadesHijasAgregadas.indexOf(subUnidad),1);
                }
            }
        },
        sumarHorasTotales: function(){
            this.newDesign.horas_totales=this.newDesign.horas_presenciales + this.newDesign.horas_autonomas
        },
        sumarUnidad: function(){
            this.horasTotalUni=this.horasPresencialesUni + this.horasAutonomasUni
        },
        sumarUpdateUni: function(){
            this.newhorasTotalUni=this.newhorasPresencialesUni + this.newhorasAutonomasUni
        },
        sumarSubUnidad: function(){
            this.horasTotalSubUni=this.horasPresencialesSubUni + this.horasAutonomasSubUni
        },
        sumarUpdateSub: function(){
            this.newhorasTotalSubUni=this.newhorasPresencialesSubUni + this.newhorasAutonomasSubUni
        },
        getAreas: function(){
            axios.get('/academico/api/area/').then((response)=>{
                this.areas=response.data;
            }).catch((err)=>{
                console.log(err)
            })
        },
        getEspecialidades: function () {
            axios.get('/academico/api/especialidad/').then((response)=>{
                this.especialidades=response.data;
            }).catch((err)=>{
                console.log(err)
            })
        },
        // getObjetivosEspecificos: function(){
        //     axios.get('/academico/api/objetivoEspecifico/').then((response)=>{
        //         this.objEspecificos=response.data;
        //         console.log(this.objEspecificos);
        //     }).catch((err)=>{
        //         console.log(err)
        //     });
        // },
        // getTipoEvento: function () {
        //     axios.get('/academico/api/tipoEvento/').then((response)=>{
        //         this.tipoEvento=response.data;
        //     }).catch((err)=>{
        //         console.log(err)
        //     })
        // },
        createObjEspecifico: function () {
            this.objEspecificos.push({
                'descripcion':this.crearObjEspecifico,
                "design":null
            });
            this.crearObjEspecifico=""
        },
        verUpdateObj: function (index) {
            this.indexUpdateObj=index;
            this.newObjEspecifico=this.objEspecificos[index].descripcion;
            this.formActualizarObj=true
        },
        borrarObj: function (index) {
            this.objEspecificos.splice(index,1)
        },
        guardarUpdateObj: function (index) {
            this.formActualizarObj=false;
            this.objEspecificos[index].descripcion=this.newObjEspecifico;
        },
        createUnidad: function(){
            this.unidades.push({
                "numero": null,
                "nombre_unidad": this.detalleUnidad,
                "horas_presenciales_unidad": this.horasPresencialesUni,
                "horas_autonomas_unidad": this.horasAutonomasUni,
                "horas_totales": this.horasTotalUni,
                "objetivo": this.objetivoUni,
                "design": null
            })
            
        },
        vaciarCamposUnidades: function(){
            this.detalleUnidad="",
            this.horasPresencialesUni=null,
            this.horasAutonomasUni=null,
            this.horasTotalUni=null,
            this.objetivoUni=""
            $("#actualizarUnidad").modal("hide")
        },
        verUpdateUnidad: function(index){
            this.numUnidadUpdate=index
            this.newdetalleUnidad=this.unidades[index].nombre_unidad
            this.newhorasPresencialesUni=this.unidades[index].horas_presenciales_unidad
            this.newhorasAutonomasUni=this.unidades[index].horas_autonomas_unidad
            this.newhorasTotalUni=this.unidades[index].horas_totales
            this.newobjetivoUni=this.unidades[index].objetivo
            this.formActualizarUni=true
            $("#actualizarUnidad").modal("show")
        },
        guardarUpdateUnidad: function(){
            var cambioUnidad=this.unidades[this.numUnidadUpdate].nombre_unidad
            this.unidades[this.numUnidadUpdate].nombre_unidad=this.newdetalleUnidad
            this.unidades[this.numUnidadUpdate].horas_presenciales_unidad=this.newhorasPresencialesUni
            this.unidades[this.numUnidadUpdate].horas_autonomas_unidad=this.newhorasAutonomasUni
            this.unidades[this.numUnidadUpdate].horas_totales=this.newhorasTotalUni
            this.unidades[this.numUnidadUpdate].objetivo=this.newobjetivoUni
            this.formActualizarUni=false
            for (let index = 0; index < this.subUnidades.length; index++) {
        
                if(this.subUnidades[index].unidad===cambioUnidad){
                    this.subUnidades[index].unidad=this.newdetalleUnidad
                }
            }
            this.newdetalleUnidad=""
            this.newhorasPresencialesUni=null
            this.newhorasAutonomasUni=null
            this.newhorasTotalUni=null
        },
        borrarUnidad:function(index){
            var eliminar=this.unidades[index].nombre_unidad
            for (let indice = this.subUnidades.length-1; indice >= 0 ; indice--) {
                if(eliminar===this.subUnidades[indice].unidad){
                    this.borrarSubUnidad(indice)
                }
            }
            this.unidades.splice(index,1)
        },
        
        createUnidadSub: function(){
            if(this.formActualizarUni){
                this.subUnidades.push({
                    "numero_sub": "",
                    "nombre_sub": this.detalleSubUnidad,
                    "horas_presenciales_sub": this.horasPresencialesSubUni,
                    "horas_autonomas_sub": this.horasAutonomasSubUni,
                    "horas_totales_sub": this.horasTotalSubUni,
                    "unidad": this.newdetalleUnidad,
                    "design": null
                })
            }else{
                this.subUnidades.push({
                    "numero_sub": "",
                    "nombre_sub": this.detalleSubUnidad,
                    "horas_presenciales_sub": this.horasPresencialesSubUni,
                    "horas_autonomas_sub": this.horasAutonomasSubUni,
                    "horas_totales_sub": this.horasTotalSubUni,
                    "unidad": this.detalleUnidad,
                    "design": null
                })
            }
            this.detalleSubUnidad="",
            this.horasPresencialesSubUni=null,
            this.horasAutonomasSubUni=null,
            this.horasTotalSubUni=null
        },
        verUpdateSubUnidad: function(index){
            this.indexSubUnidad=index
            this.newdetalleSubUnidad=this.subUnidades[index].nombre_sub
            this.newhorasPresencialesSubUni=this.subUnidades[index].horas_presenciales_sub
            this.newhorasAutonomasSubUni=this.subUnidades[index].horas_autonomas_sub
            this.newhorasTotalSubUni=this.subUnidades[index].horas_totales_sub
            this.formActualizarSubUni=true
        },
        borrarSubUnidad: function(index){
            this.subUnidades.splice(index,1)
        },
        guardarUpdateSubUnidad : function(index){
            this.formActualizarSubUni=false
            this.subUnidades[index].nombre_sub=this.newdetalleSubUnidad
            this.subUnidades[index].horas_presenciales_sub=this.newhorasPresencialesSubUni
            this.subUnidades[index].horas_autonomas_sub=this.newhorasAutonomasSubUni
            this.subUnidades[index].horas_totales_sub=this.newhorasTotalSubUni
        },
        createRecurso: function () {
            this.recursos.push({
                "tipo": this.tipoRecurso,
                "descripcion": this.descripcionRecurso,
                "design": null
            })
            this.tipoRecurso=""
            this.descripcionRecurso=""
            $("#staticBackdropRecurso").modal("hide")
        },
        verUpdateRecurso: function (index) {
            this.indexUpdateRecurso=index
            this.newtipoRecurso=this.recursos[index].tipo
            this.newdescripcionRecurso=this.recursos[index].descripcion
            this.formActualizarRecurso=true
            $("#staticBackdropRecurso").modal("show")
        },
        guardarUpdateRecurso: function () {
            this.recursos[this.indexUpdateRecurso].tipo=this.newtipoRecurso
            this.recursos[this.indexUpdateRecurso].descripcion=this.newdescripcionRecurso
            this.newtipoRecurso=""
            this.newdescripcionRecurso=""
            this.formActualizarRecurso=false
            $("#staticBackdropRecurso").modal("hide")
        },
        borrarRecurso: function (index) {
            this.recursos.splice(index,1)
        },
        createReferencia: function () {
          this.referencias.push({
            "tipo": this.tipoReferencia,
            "titulo": this.tituloReferencia,
            "autor": this.autorReferencia,
            "sitio_web": this.sitioReferencia,
            "enlace": this.enlaceReferencia,
            "publicacion": this.publicacionReferencia,
            "editorial": this.editorialReferencia,
            "pais": this.paisReferencia,
            "fecha": this.consultaReferencia,
            "descripcion": this.descripcionReferencia,
            "design": null
          })
          this.tipoReferencia="Libro"
          this.tituloReferencia=""
          this.autorReferencia=""
          this.publicacionReferencia=""
          this.editorialReferencia=""
          this.paisReferencia=""
          this.consultaReferencia=""
          this.sitioReferencia=""
          this.enlaceReferencia=""
          this.descripcionReferencia=""
          $("#staticBackdropReferencias").modal("hide")
        },
        verUpdateReferencia: function (index) {
            this.indexUpdateReferencia=index
            this.newtipoReferencia=this.referencias[index].tipo
            this.newtituloReferencia=this.referencias[index].titulo
            this.newautorReferencia=this.referencias[index].autor
            this.newpublicacionReferencia=this.referencias[index].publicacion,
            this.neweditorialReferencia=this.referencias[index].editorial,
            this.newpaisReferencia=this.referencias[index].pais,
            this.newconsultaReferencia=this.referencias[index].fecha,
            this.newsitioReferencia=this.referencias[index].sitio_web
            this.newenlaceReferencia=this.referencias[index].enlace
            this.newdescripcionReferencia=this.referencias[index].descripcion
            this.formActualizarReferencia=true
            $("#staticBackdropReferencias").modal("show")
        },
        guardarUpdateReferencia: function () {
            this.referencias[this.indexUpdateReferencia].tipo=this.newtipoReferencia
            this.referencias[this.indexUpdateReferencia].titulo=this.newtituloReferencia
            this.referencias[this.indexUpdateReferencia].autor= this.newautorReferencia
            this.referencias[this.indexUpdateReferencia].publicacion=this.newpublicacionReferencia
            this.referencias[this.indexUpdateReferencia].editorial=this.neweditorialReferencia
            this.referencias[this.indexUpdateReferencia].pais=this.newpaisReferencia
            this.referencias[this.indexUpdateReferencia].fecha=this.newconsultaReferencia
            this.referencias[this.indexUpdateReferencia].sitio_web=this.newsitioReferencia
            this.referencias[this.indexUpdateReferencia].enlace=this.newenlaceReferencia
            this.referencias[this.indexUpdateReferencia].descripcion=this.newdescripcionReferencia
            this.newtipoReferencia=""
            this.newtituloReferencia=""
            this.newautorReferencia=""
            this.newpublicacionReferencia=""
            this.neweditorialReferencia=""
            this.newpaisReferencia=""
            this.newconsultaReferencia=""
            this.newsitioReferencia=""
            this.newenlaceReferencia=""
            this.newdescripcionReferencia=""
            this.formActualizarReferencia=false
            $("#staticBackdropReferencias").modal("hide")
        },
        borrarReferencia: function (index) {
            this.referencias.splice(index,1)
        },
        createLectura: function () {
            this.lecturas.push({
                "tipo": this.tipoLectura,
                "titulo": this.tituloLectura,
                "autor": this.autorLectura,
                "sitio_web": this.sitioLectura,
                "enlace": this.enlaceLectura,
                "publicacion": this.publicacionLectura,
                "editorial":this.editorialLectura ,
                "pais": this.paisLectura,
                "fecha": this.consultaLectura,
                "descripcion": this.descripcionLectura,
                "design": null
            })
            this.tipoLectura="Libro"
            this.tituloLectura=""
            this.autorLectura=""
            this.publicacionLectura=null
            this.editorialLectura=""
            this.paisLectura=""
            this.consultaLectura=""
            this.sitioLectura=""
            this.enlaceLectura=""
            this.descripcionLectura=""
            $("#staticBackdropLecturas").modal("hide")
        },
        verUpdateLectura: function (index) {
            this.indexUpdateLectura=index
            this.newtipoLectura=this.lecturas[index].tipo
            this.newtituloLectura=this.lecturas[index].titulo
            this.newautorLectura=this.lecturas[index].autor
            this.newpublicacionLectura=this.lecturas[index].publicacion
            this.neweditorialLectura=this.lecturas[index].editorial
            this.newpaisLectura=this.lecturas[index].pais
            this.newconsultaLectura=this.lecturas[index].fecha
            this.newsitioLectura=this.lecturas[index].sitio_web
            this.newenlaceLectura=this.lecturas[index].enlace
            this.newdescripcionLectura=this.lecturas[index].descripcion
            this.formActualizarLectura=true
            $("#staticBackdropLecturas").modal("show")
        },
        guardarUpdateLectura(){
            this.lecturas[this.indexUpdateLectura].tipo=this.newtipoLectura
            this.lecturas[this.indexUpdateLectura].titulo=this.newtituloLectura
            this.lecturas[this.indexUpdateLectura].autor=this.newautorLectura
            this.lecturas[this.indexUpdateLectura].publicacion=this.newpublicacionLectura
            this.lecturas[this.indexUpdateLectura].editorial=this.neweditorialLectura
            this.lecturas[this.indexUpdateLectura].pais=this.newpaisLectura
            this.lecturas[this.indexUpdateLectura].fecha=this.newconsultaLectura
            this.lecturas[this.indexUpdateLectura].sitio_web=this.newsitioLectura
            this.lecturas[this.indexUpdateLectura].enlace=this.newenlaceLectura
            this.lecturas[this.indexUpdateLectura].descripcion=this.newdescripcionLectura
            this.newtipoLectura=""
            this.newtituloLectura=""
            this.newautorLectura=""
            this.newpublicacionLectura=null
            this.neweditorialLectura=""
            this.newpaisLectura=""
            this.newconsultaLectura=""
            this.newsitioLectura=""
            this.newenlaceLectura=""
            this.newdescripcionLectura=""
            this.formActualizarLectura=false
            $("#staticBackdropLecturas").modal("hide")
        },
        borrarLectura: function (index) {
          this.lecturas.splice(index,1)  
        },
        realizarPost: async function (url,objeto,mensaje) {
            await axios.post(url,objeto).then((response)=>{
                console.log(mensaje);
                return response;
            }).catch((err)=>{
                console.log(err.response)
            })
            
        },
        // obtenerObjEsp:function(objeto,id, index) {
        //     axios.get('/academico/api/objetivoEspecifico/?desc='+objeto.objetivo).then((response)=>{
        //         this.objetivo_sub=response.data;
        //         console.log(this.objetivo_sub);
        //         objeto.numero=index+1
        //         objeto.design=id
        //         objeto.objetivo=this.objetivo_sub.id
        //         this.realizarPost('/academico/api/unidad/',this.unidades[index])
        //         this.objetivo_sub={}
        //     }).catch((err)=>{
        //         console.log(err)
        //     })
        // },
        obtenerUnidad: async function(unidad) {
            await axios.get('/academico/api/unidad/?nom='+unidad).then((response)=>{
                this.tempuni=response.data;
                return response;
            }).catch((err)=>{
                console.log(err)
            })
        },
        guardarObjetivos: async function (id) {
            for(let indexobj=0; indexobj < this.objEspecificos.length; indexobj++){
                this.objEspecificos[indexobj].design=id;
                this.realizarPost('/academico/api/objetivoEspecifico/',this.objEspecificos[indexobj],"se realizo el post de objetivo"+this.objEspecificos[indexobj].descripcion);
            }
        },
        guardarUnidades: async function (id) {
            for (let index = 0; index < this.unidades.length; index++){
                await axios.get('/academico/api/objetivoEspecifico/?desc='+this.unidades[index].objetivo).then((response)=>{
                    this.objetivo_sub=response.data;
                    console.log(this.objetivo_sub);
                    this.unidades[index].numero=index+1;
                    this.unidades[index].design=id;
                    this.unidades[index].objetivo=this.objetivo_sub[0].id;
                    this.realizarPost('/academico/api/unidad/',this.unidades[index],"se realizo el post de unidad"+this.unidades[index].nombre_unidad);
                    this.objetivo_sub={}
                }).catch((err)=>{
                    console.log(err);
                })
            }  
        },
        guardarSubUnidad: async function (id) {
            for (let indexuni = 0; indexuni < this.unidades.length; indexuni++){
                var lista_obj=[]
                var cont = 1
                for (let indexsub = 0; indexsub < this.subUnidades.length; indexsub++){
                    if(this.unidades[indexuni].nombre_unidad === this.subUnidades[indexsub].unidad){
                        lista_obj.push(this.subUnidades[indexsub]);
                    }
                }
                await this.obtenerUnidad(this.unidades[indexuni].nombre_unidad)
                for (let indexlist = 0; indexlist < lista_obj.length; indexlist++){
                    lista_obj[indexlist].numero_sub=this.tempuni.numero.toString()+"."+cont.toString();
                    lista_obj[indexlist].unidad=this.tempuni.numero;
                    lista_obj[indexlist].design=id;
                    await this.realizarPost('/academico/api/subUnidad/',lista_obj[indexlist],"se realizo el post de subunidad");
                    cont++;
                }
                lista_obj=[]
                cont=1
                this.tempuni={}
            }
        },
        guardarRecurso:function (id) {
            for(let indexrec=0; indexrec < this.recursos.length; indexrec++){
                this.recursos[indexrec].design=id
                this.realizarPost('/academico/api/recurso/',this.recursos[indexrec],"se realizo el post de recurso")
            }
        },
        guardarLectura:function (id) {
            for(let indexlec=0; indexlec < this.lecturas.length; indexlec++){
                this.lecturas[indexlec].design=id
                this.realizarPost('/academico/api/lectura/',this.lecturas[indexlec],"se realizo el post de lectura")
            }
        },
        guardarReferencia:function (id) {
            for(let indexref=0; indexref < this.referencias.length; indexref++){
                this.referencias[indexref].design=id
                this.realizarPost('/academico/api/referencia/',this.referencias[indexref],"se realizo el post de referencia")
            }  
        },
        obtenerCodigoNuevo: function(){
            this.ultimoIdDiseno = this.disenos.length+1;
            if(this.ultimoIdDiseno<100 && this.ultimoIdDiseno>=10){
                this.ultimoIdDiseno = "0"+this.ultimoIdDiseno;
            }else if(this.ultimoIdDiseno<10){
                this.ultimoIdDiseno = "00"+this.ultimoIdDiseno;
            }
            for(esp of this.especialidades){
                if(esp.id == this.newDesign.especialidad){
                    this.codeEsp = esp.codigo;
                }
            }
            this.newDesign.codigo = this.codeEsp+this.codeTipo+this.ultimoIdDiseno;
        },
        crearObjetoPadreHijo: function(id){
            for(hijo of this.disenosHijosAgregados){
                axios.post('/api/disenoPadreHijo/',
                    {'padre':id,'hijo':hijo.id}).then((response)=>{
                }).catch((err)=>{
                    console.log(err)
                })
            }

        },
        editarCodeProgHijo: function(){
            for(hijo of this.disenosHijosAgregados){
                axios.patch('/academico/api/design/'+hijo.id+'/',
                    {cod_programa:this.newDesign.codigo}).then((response)=>{
                }).catch((err)=>{
                    console.log(err.response)
                })
            }
        },
                // obtenerDesign:function() {
        //     axios.get('/academico/api/design/?cod='+this.newDesign.codigo).then((response)=>{
        //         this.designtemp=response.data;
        //         console.log(this.designtemp);
        //     }).catch((err)=>{
        //         console.log(err)
        //     })
        // },
        createDesign: function() {
            this.obtenerCodigoNuevo();
            axios.post('/academico/api/design/',this.newDesign).then((response)=>{
                if(!this.padre){            //no es necesario crear nuevas instancias de los objetivos especificos, unidades y subunidades, solo se los obtiene de los hijos
                    this.guardarObjetivos(response.data.id);
                    this.guardarUnidades(response.data.id);
                    this.guardarSubUnidad(response.data.id);
                }else{
                    this.crearObjetoPadreHijo(response.data.id);
                    this.editarCodeProgHijo();
                }
                this.guardarRecurso(response.data.id);
                this.guardarLectura(response.data.id);
                this.guardarReferencia(response.data.id);
                $("#modalExito").modal();
            }).catch((err)=>{
                console.log(err.response)
            })

            
        }
    }
})
