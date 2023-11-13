import { render } from 'preact';
import './style.css';

export function App() {
	return (
		<>
      <header>
        <Indicator title='Sağlık' value={30} />
        <Indicator title='Asker' value={60} />
        <Indicator title='Din' value={10} />
        <Indicator title='Yiyecek' value={40} />
      </header>
			<section>
        <div class='card'>ABC</div>
      </section>
		</>
	);
}

function Indicator({title, value}) {
  const wstr = 'width:' + value + '%'
  return (
    <div class='indicator'>
      <p>{title}</p>
      <div class='pbar'>
        <div style={wstr}></div>
      </div>
    </div>
  )
}

render(<App />, document.getElementById('app'));
