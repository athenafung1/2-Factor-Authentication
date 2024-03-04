import time

# pip install pyotp
import pyotp

# pip install qrcode
import qrcode


''' KEYS: anyone with the same key will generate the same OTPs '''
def generate_key(random):
    # Generating a random key
    if random:
        key = pyotp.random_base32()

    # Manually creating key
    key = "WiCySSuperSuperSecretKey"
    
    return key


''' OTPs: one-time passwords for authentication '''
 
# Time-based OTP: every 30 seconds, generate a new OTP
def generate_time_based_OTP(key, test = False):
    totp = pyotp.TOTP(key)
    current_OTP = totp.now() # A binascii.Error is raised if input key is incorrectly padded or if there are non-alphabet characters present in the input.
    print(f"Your current time-based OTP is: {current_OTP}")

    if test:
        print("\nWaiting for 30 seconds ...")
        time.sleep(30)

        if not totp.verify(current_OTP):
            print(f"Your OTP, {current_OTP}, has changed!")
            print(f"New OTP: {totp.now()}")

    return current_OTP

# Counter-based OTP: OTP at each index will always be the same, given the same key
def generate_counter_based_OTPs(key, num_counters, test = False):
    hotp = pyotp.HOTP(key)
    print("Your current counter-based OTPs are: ")
    OTPs = {}
    for i in range(num_counters):
        current_OTP = hotp.at(i)
        OTPs[i] = current_OTP

        print(f"At counter {i}, OTP is {current_OTP}")

    if test:
        print("\n")
        for counter in range(num_counters):
            user_input = input(f"Enter 2FA Code for counter {counter}: ")
            if hotp.verify(user_input, counter):
                print("You have been authenticated!")
            else:
                print("Wrong!")

    return OTPs

def generate_totp_qrcode(my_key):
    uri = pyotp.totp.TOTP(my_key).provisioning_uri(name = "me", issuer_name="WiCyS Super Secure 2FA Workshop")
    qrcode.make(uri).save("totp_qrcode.png")

def use_qrcode(my_key):
    totp = pyotp.TOTP(my_key)
    while True:
        user_input = input("Enter 2FA code: ")
        if totp.verify(user_input):
            print("You have been authenticated!")
            break
        else:
            print("Please try again!")

def main(): 
    my_key = generate_key(random = False)

    ''' Time-based OTP '''
    current_OTP = generate_time_based_OTP(my_key, test=False)

    ''' Counter-based OTP '''
    OTPs = generate_counter_based_OTPs(my_key, 5, test=False)

    ''' URI (Uniform Resource Identifier) 
        Unique sequence of characters that identifies and distinguishes
        abstract or physical resources. Example: a URL (distinguishes resource LOCATIONS on Internet)
    '''
    qrcode = generate_totp_qrcode(my_key)
    use_qrcode (my_key)
    


if __name__ == "__main__":
    print("Starting 2FA ...\n\n")
    main()
    print("\n\nFinishing 2FA")