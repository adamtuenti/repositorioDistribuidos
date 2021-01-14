import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { DetalleCursoPageRoutingModule } from './detalle-curso-routing.module';

import { DetalleCursoPage } from './detalle-curso.page';
import { FusionChartsModule } from "angular-fusioncharts";

import * as FusionCharts from "fusioncharts";
import * as charts from "fusioncharts/fusioncharts.charts";
import * as FusionTheme from "fusioncharts/themes/fusioncharts.theme.fusion";
FusionChartsModule.fcRoot(FusionCharts, charts, FusionTheme);
@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    DetalleCursoPageRoutingModule,
    FusionChartsModule
  ],
  declarations: [DetalleCursoPage]
})
export class DetalleCursoPageModule {}
