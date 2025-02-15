import os
import uuid
import utm


def save_uploaded_file(file, upload_dir, allowed_mimetypes, file_extension=None):
    """
    Helper function to save an uploaded file to the specified directory.

    :param file: The file to be uploaded
    :param upload_dir: Directory where the file should be saved
    :param allowed_mimetypes: List of allowed mimetypes for the file
    :param file_extension: Optional extension for the file
    :return: Filename if successfully saved, else None
    """
    # Check if the file's mimetype is allowed
    if file.mimetype in allowed_mimetypes:
        # Generate a unique filename using UUID
        if not file_extension:
            file_extension = os.path.splitext(file.filename)[1]
        filename = str(uuid.uuid4()).replace('-', '')[:12] + file_extension

        # Ensure the upload directory exists
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Construct the full file path
        file_path = os.path.join(upload_dir, filename)

        # Save the file
        file.save(file_path)

        return filename
    else:
        return None
    
def utm_converter(utm_y, utm_x):
    zone_number = 38
    zone_letter = 'N'
    has_dot_utm_y = '.' in utm_y
    has_dot_utm_x = '.' in utm_x
    

    if has_dot_utm_y and not has_dot_utm_x:
        return None, None
    elif has_dot_utm_x and not has_dot_utm_y:
        return None, None
    elif not has_dot_utm_y and not has_dot_utm_x:
        return utm.to_latlon(int(utm_x), int(utm_y), zone_number, zone_letter)
    else:
        return float(utm_y), float(utm_x)
