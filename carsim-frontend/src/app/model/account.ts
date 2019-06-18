import {Coordinate} from './coordinate';

export class Account {
  id: string;
  name: string;
  start?: Coordinate;
  end?: Coordinate;
  canBeDriver: boolean;
}
