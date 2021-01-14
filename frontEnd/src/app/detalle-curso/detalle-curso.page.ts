import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { environment } from '../../environments/environment';
import { AppComponent } from '../app.component';
import * as $ from "jquery";


const data_asistencias = {
  chart: {
    showpercentvalues: "1",
    aligncaptionwithcanvas: "0",
    captionpadding: "0",
    decimals: "1",
    showlegend: "0",
    plottooltext:
      "<b>$percentValue</b> de <b>$label</b>",
    centerlabel: "$percentValue",
    theme: "fusion"
  },
  data: null
};

const data_calificaciones = {
  chart: {
    theme: "fusion",
    data: null
  }
};

const data_asistencias_line = {
  chart: {
    theme: "fusion",
    rotatelabels: "1",
    setadaptiveymin: "1",
    data: null
  }
}


@Component({
  selector: 'app-detalle-curso',
  templateUrl: './detalle-curso.page.html',
  styleUrls: ['./detalle-curso.page.scss'],
})
export class DetalleCursoPage{
  chart_asistencias: any;
  chart_calificaciones: any;
  chart_asistencias_line: any;
  detalles: any = "";
   mostrarAsistencia: boolean;
  mostrarCalificaciones: boolean;

  constructor(private router: ActivatedRoute,private App: AppComponent) {
    this.chart_asistencias = data_asistencias;
    this.chart_calificaciones = data_calificaciones;
    this.chart_asistencias_line = data_asistencias_line;
  }


  ionViewDidEnter() {
    this.mostrarAsistencia = true;
    this.mostrarCalificaciones = false;
    this.router.params.subscribe(param => {
    this.getDetalle(param['id_curso']);
    })
  }

  async getDetalle(codigo_evento:any) {
    /*
    this.detalles = await this.cursos.getDetalleCurso(id_curso);
    this.chart_asistencias.data = this.detalles.data_asistencias;
    this.chart_calificaciones.data = this.detalles.data_calificaciones;
    this.chart_asistencias_line.data=this.detalles.data_asistencias_line;
    */
   var data = {"id_participante":this.App.id_User,"codigo_evento":codigo_evento}
   var self=this;
   await $.post(environment.url +"/api/detalles_curso/",data).done(function (res) {
     if(!res.error){
     self.detalles=res.detalles
     self.detalles.imagen = environment.url + self.detalles.imagen
     console.log(self.detalles)
     }
   })
  }

  segmentChanged(ev: any) {
    if (ev.target.value == "asistencias") {
      this.mostrarAsistencia = true;
      this.mostrarCalificaciones = false;
    }
    if (ev.target.value == "calificaciones") {
      this.mostrarCalificaciones = true;
      this.mostrarAsistencia = false;
    }
  }


}