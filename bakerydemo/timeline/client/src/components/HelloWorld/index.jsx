import { PureComponent } from 'react'; // eslint-disable-line import/no-extraneous-dependencies
import { string } from 'prop-types'; // eslint-disable-line import/no-extraneous-dependencies
import classNames from 'classnames';

const generateColor = () => {
  const random = Math.random() * 0xffffff;
  return `#${(0x1000000 + random).toString(16).substr(1, 6)}`;
};

export default class HelloWorld extends PureComponent {
  static defaultProps = {
    className: '',
    initialColor: '#000',
  };

  static propTypes = {
    className: string,
    initialColor: string,
  };

  state = {
    color: this.props.initialColor,
  };

  componentWillReceiveProps({ initialColor }) {
    if (initialColor !== this.props.initialColor) {
      this.setState({ color: initialColor });
    }
  }

  handleClick = () => {
    this.setState({
      color: generateColor(),
    });
  };

  render() {
    return (
      <div className={classNames('component', this.props.className)}>
        <h1 style={{ color: this.state.color, padding: '20px' }}>
          Hello World!
        </h1>
        <button onClick={this.handleClick}>Change color</button>
      </div>
    );
  }
}
