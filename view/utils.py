import re


class Utility:

    def email_validate(self, email):
        """Here email validation is done"""
        if re.match(f"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False

    def validate_file_extension(self, data):
        import os
        ext = os.path.splitext(data['profile_path'])[1]  # [0] returns path+filename
        valid_extensions = ['.jpg']
        if not ext.lower() in valid_extensions:
            print("Unsupported file extension.")
        else:
            return True
            # raise ValidationError(u'Unsupported file extension.')

    def validate_file_size(self, data):
        filesize = len(data['profile_path'])
        if filesize > 10485760:
            print("The maximum file size that can be uploaded is 10MB")
        else:
            return True