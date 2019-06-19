import {Component, OnDestroy, OnInit} from '@angular/core';
import {AccountService} from '../../service/account.service';
import {ActivatedRoute} from '@angular/router';
import {Trip} from '../../model/trip';



@Component({
  selector: 'app-trip',
  templateUrl: './trip.component.html',
  styleUrls: ['./trip.component.scss']
})
export class TripComponent implements OnInit, OnDestroy {



  constructor(private activatedRouter: ActivatedRoute,
              private accountService: AccountService) {
  }

  ngOnInit() {

  }

  ngOnDestroy(): void {

  }

}
