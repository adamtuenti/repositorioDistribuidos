import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'educ',
    component: TabsPage,
    children: [
      {
        path: 'home',
        loadChildren: () => import('../home/home.module').then(m => m.HomePageModule)
      },
      {
        path: 'cursos',
        children: [{
          path: "",
          loadChildren: () => import('../cursos/cursos.module').then(m => m.CursosPageModule),
        },
        {
          path: ':id_curso',
          loadChildren: () => import('../detalle-curso/detalle-curso.module').then(m => m.DetalleCursoPageModule)
        }]

      },
      {
        path: 'notificaciones',
        loadChildren: () => import('../notificaciones/notificaciones.module').then(m => m.NotificacionesPageModule)
      },
      {
        path: 'encuestas',
        loadChildren: () => import('../encuestas/encuestas.module').then(m => m.EncuestasPageModule)
      },
      {
        path: 'contacto',
        loadChildren: () => import('../contacto/contacto.module').then(m => m.ContactoPageModule)
      },
      {
        path: 'sugerencias',
        loadChildren: () => import('../sugerencias/sugerencias.module').then(m => m.SugerenciasPageModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TabsPageRoutingModule { }
