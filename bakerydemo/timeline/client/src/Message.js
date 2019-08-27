import React from 'react';
import PropTypes from 'prop-types';

/**
 * A verbose example of a Functional component. Message renders the loading or
 * error message states.
 * @param {Object} props
 */
const Message = ({ error, isLoading }) => (
  <div className="messages">
    <ul>
      {isLoading && <li className="success">Loading...</li>}
      {error && <li className="error">Error: {error.message}</li>}
    </ul>
  </div>
);

Message.defaultProps = {
  isLoading: false,
  error: {},
};

Message.propTypes = {
  isLoading: PropTypes.bool,
  error: PropTypes.shape({
    message: PropTypes.string,
  }),
};

export default Message;
