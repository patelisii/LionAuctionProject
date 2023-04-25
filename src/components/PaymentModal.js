import React, { useState, useContext, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button } from '@mui/material';
import UserContext from "./UserContext";
const PaymentModal = ({ open, onClose, onSubmitPayment }) => {
  const [cardNumber] = useState('');
  const [cardExpiry] = useState('');
  const [cardCVV] = useState('');
  const [cardInfo, setCardInfo] = useState({ cardNumber: '', cardExpiry: '', cardCVV: '' });
  const {userEmail} = useContext(UserContext);
  const handlePaymentSubmit = () => {
    // Call the onSubmitPayment function with the card details
    onSubmitPayment({
      cardNumber,
      cardExpiry,
      cardCVV,
    });

    // Close the modal
    onClose();
  };
   useEffect(() => {
      if (open) {
        const fetchCreditCardInfo = async () => {
          const response = await fetch("http://127.0.0.1:5000/get_credit_card", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: userEmail }),
          });

          const data = await response.json();

          if (data.success) {
            const [ cardNumber, cardExpiry, cardCVV ] = data.card;
            setCardInfo({ cardNumber, cardExpiry, cardCVV });

          }
        };

        fetchCreditCardInfo();
      }
    }, [open, userEmail]);

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Complete Transaction</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          id="cardNumber"
          label="Card Number"
          type="text"
          fullWidth
          variant="standard"
          value={cardInfo.cardNumber}
          onChange={(e) => setCardInfo({ ...cardInfo, cardNumber: e.target.value })}
        />
        <TextField
          margin="dense"
          id="cardExpiry"
          label="Expiry Date (MM/YY)"
          type="text"
          fullWidth
          variant="standard"
          value={cardInfo.cardExpiry}
          onChange={(e) => setCardInfo({ ...cardInfo, cardExpiry: e.target.value })}
        />
        <TextField
          margin="dense"
          id="cardCVV"
          label="CVV"
          type="text"
          fullWidth
          variant="standard"
          value={cardInfo.cardCVV}
          onChange={(e) => setCardInfo({ ...cardInfo, cardCVV: e.target.value })}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handlePaymentSubmit} color="primary">
          Submit Payment
        </Button>
      </DialogActions>
    </Dialog>
  );
};
export default PaymentModal;