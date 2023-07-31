'use strict';


class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    // Display a "Like" <button>
  return (
    <button onClick={() => this.setState({ liked: true })}>
      Like
    </button>
  );
  }
}

const domContainer = document.querySelector('#everything_container');
const root = ReactDOM.createRoot(domContainer);
root.render(<LikeButton />);