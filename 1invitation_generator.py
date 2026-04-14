def format_line(text, width = 46):
    if len(text) > width:
        text = text[:width-3] + "..." # Truncates the text to the width of the invitation and adds ellipsis
    
    lpadding = (width - len(text)) // 2 # Calculates the left padding
    rpadding = width - len(text) - lpadding # Calculates the right padding
    return f"* {' ' * lpadding}{text}{' ' * rpadding} *" # Returns the formatted line

def generate_invitations(guests, details):
    """
    Generates ASCII invitations for a list of guests.
    Args:
        guests (list): A list of dictionaries, where each dictionary contains 'Name', 'Affiliation', and 'Email'.
        details (dict): A dictionary containing 'Date', 'Venue', and 'Schedule'.
    Returns:
        dict: A dictionary where keys are guests' email addresses and values are their ASCII invitation strings.
    """
    border_length = 50
    invitations = {}
    
    header = "*" * border_length
    line1 = format_line("Saraswati Puja Invitation")
    line2 = format_line("Utkal Parishad, IIT Kanpur")
    empty_line = format_line("")
    
    date = f"Date: {details['Date']}"
    venue = f"Venue: {details['Venue']}"
    schedule = f"Schedule: {details['Schedule']}"
    
    for guest in guests: # Iterates through the list of guests and creates an invitation for each guest
        name = guest['Name']
        affiliation = guest['Affiliation']
        email = guest['Email']
        
        invitation_strings = [
            header,
            line1,
            line2,
            empty_line,
            format_line(f"Dear {name}"),
            format_line(affiliation),
            empty_line,
            format_line(date),
            format_line(venue),
            format_line(schedule),
            header
        ]
        
        invitations[email] = "\n".join(invitation_strings)
    
    return invitations

if __name__ == "__main__":
    guests = [
        {'Name': 'Aman', 'Affiliation': 'CSE Dept', 'Email': 'aman@iitk.ac.in'},
        {'Name': 'Dr. Very Long Name That Definitely Exceeds The Character Limit', 'Affiliation': 'Physics Dept', 'Email': 'dr.long@iitk.ac.in'}
    ]
    details = {'Date': 'Feb 14, 2026', 'Venue': 'Community Hall', 'Schedule': '10:00 AM'}
    
    results = generate_invitations(guests, details)
    for email, invite in results.items():
        print(f"Invitation for {email}:")
        print(invite)
        print(" "*50 + '\n' + " "*50 + '\n')
