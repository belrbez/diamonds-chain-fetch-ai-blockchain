import { Injectable } from '@angular/core';
import {Account} from '../model/account';

@Injectable({
  providedIn: 'root'
})
export class AccountService {

  private accounts: Account[];

  constructor() {
    this.accounts = [
      {
        id: 'id1',
        name: 'Steve Gabe'
      } as Account,
      {
        id: 'id2',
        name: 'Samantha Smith'
      } as Account
    ];
  }

  public getAccount(id: string): Account | null {
    const found = this.accounts.filter(account => account.id === id);
    if (found.length > 0) {
      return found[0];
    }
    return null;
  }
}
