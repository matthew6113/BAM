import { render } from 'preact';
import { App } from './App';
import './styles.css';

const root = document.getElementById('app')!;
// index.html holds a static title and byline for the first paint; the app draws its own in their place,
// in the same task, so nothing flashes between the two.
root.replaceChildren();
render(<App />, root);
