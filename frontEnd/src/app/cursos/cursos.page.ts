import { Component, OnInit } from '@angular/core';
import * as $ from "jquery";
import { AppComponent } from '../app.component';
import { AlertController } from '@ionic/angular';
import { Router} from '@angular/router';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-cursos',
  templateUrl: './cursos.page.html',
  styleUrls: ['./cursos.page.scss'],
})
export class CursosPage {

  listCursos = []
  constructor(private App: AppComponent, private alertController: AlertController,private router:Router) {
    
  }

  ionViewDidEnter() {
    this.listCursos = []
    
    if (this.App.id_User != null) {
      this.getCursos();
    }
   
  }
  
  async getCursos() {
    var data = {"id_participante":this.App.id_User}
    var self=this;
    await $.post(environment.url +"/api/cursos_participante/",data).done(function (res) {
      if(!res.error){
      self.listCursos=res.cursos
      for (let i = 0; i < self.listCursos.length; i++) {
        self.listCursos[i].imagen = environment.url + self.listCursos[i].imagen
      }
      }
      else{
        self.alertCurso();
      }
    })
  }


  async alertCurso() {
      const alert = await this.alertController.create({
        header: 'Mensaje',
        subHeader: 'Sin cursos registrados',
        message: 'Usted no pertenece a ningún curso',
        buttons: ['OK']
      });
  
      await alert.present();
    }
}