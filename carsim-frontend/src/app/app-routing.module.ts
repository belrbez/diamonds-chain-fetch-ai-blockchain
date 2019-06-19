import { NgModule } from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {MapComponent} from './map/map-component/map.component';
import {TripComponent} from './map/trip/trip.component';
import {NewTripComponent} from './map/new-trip/new-trip.component';

const routes: Routes = [
  { path: 'map/:id', component: MapComponent,
  children: [
    {
      path: 'new-trip', component: NewTripComponent
    },
    {
      path: 'trips/:tripId', component: TripComponent
    }
  ]},
  { path: '',
    redirectTo: '/map/id1/new-trip',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
