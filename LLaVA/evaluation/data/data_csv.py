import csv
import os

def create_csv(image_paths, predicted_captions, ground_truth_captions, output_file):
    """
    Create a CSV file with image paths, predicted captions, and ground truth captions.

    :param image_paths: List of paths to the images.
    :param predicted_captions: List of predicted captions corresponding to the images.
    :param ground_truth_captions: List of ground truth captions corresponding to the images.
    :param output_file: Path to the output CSV file.
    """
    # Check that the input lists have the same length
    if not (len(image_paths) == len(predicted_captions) == len(ground_truth_captions)):
        raise ValueError("All input lists must have the same length")

    # Create the CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['image_path', 'predicted_caption', 'ground_truth_caption'])
        
        for img_path, pred_caption, gt_caption in zip(image_paths, predicted_captions, ground_truth_captions):
            writer.writerow([img_path, pred_caption, gt_caption])

    print(f"CSV file '{output_file}' created successfully.")

# Example usage
if __name__ == "__main__":
    # Example lists (replace these with your actual data)
    image_paths = [
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/green lapcot.png',
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/high.png',
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/lambo watch.jpg',
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/mosque t-shirt.jpg',
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/NIKE.jpg',
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/puma girl sneakers.jpg',
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/red suit.png',
        '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/sea short.jpg',
        "/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/syria t-shirt.jpg",
        "/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data/images/tomato shirt.png"
    ]
    predicted_captions_original = [
        "a green coat, which is a long, oversized coat with a belt.",
        'a pair of black boots. The boots have a lace-up design and are likely made of leather.',
        "a watch, specifically a black and gold watch with a black face and a gold band. The watch features a unique design with two clocks on the face, which adds a distinctive and luxurious touch to it",
        "a black t-shirt featuring a colorful design of a cityscape with a mosque and a clock tower.",
        'a pair of Nike shoes. The shoes are white and blue in color, and they are covered in a variety of colorful balls, which are likely bouncy balls.',
        'a black and gold shoe, which appears to be a sneaker. The shoe is placed on a pink surface, possibly a carpet or a bed.',
        'a red suit jacket, which is a part of a mans formal attire. The suit jacket is paired with a black vest and a bow tie.',
        'a pair of swim trunks, which are a type of shorts designed for swimming and other water-related activities. The swim trunks are colorful and feature a pattern of tropical leaves, giving them a vibrant and eye-catching appearance.',
        'a t-shirt featuring a mushroom and a reference to Syria Mosque. The t-shirt is white and has a design that includes a red mushroom, green writing, and a star. The design is likely related to a band or a specific event, as it is described as a "band shirt."',
        'a white shirt featuring a design of various fruits and vegetables. The design includes a tomato, an orange, a carrot, a peach, and a grape.'
    ]

    predicted_captions_ours = [
        "Bright green, oversized coat with a belt, featuring wide lapels and black buttons.",
        "Black knee-high boots with a lace-up design, likely made of leather, and a back tie detail.",
        "Black and gold watch with a black face and gold band, featuring two clocks and a luxurious design.",
        "Black t-shirt with a colorful cityscape design including a mosque and a clock tower.",
        "White Nike shoes with colorful balls, blue Nike logo, and orange accents.",
        "Black and gold sneaker placed on a pink surface, possibly a carpet or bed.",
        "Red suit jacket paired with a black vest and bow tie, part of a man's formal attire.",
        "Colorful swim trunks with a pattern of tropical leaves, designed for swimming activities.",
        "White t-shirt with a mushroom and a reference to Syria Mosque, likely a band shirt with a red mushroom, green writing, and a star.",
        "White shirt with a design of various fruits and vegetables including a tomato, an orange, a carrot, a peach, and a grape."
    ]

    ground_truth_captions = [
        "Bright green, oversized, double-breasted overcoat with wide lapels and black buttons.",
        'Black knee-high boots with low heels and back tie detail.',
        "Luxury Lamborghini watch with black and gold accents, three sub-dials, and leather strap.",
        "Black t-shirt with colorful mosque design and small circular logo on the chest.",
        "White Nike sneaker with colorful sole, orange accents, and blue Nike logo.",
        'Black Puma sneakers with gold accents, elastic straps, and a chunky sole design.',
        'Elegant red and black tuxedo with floral pattern, bow tie, chain accessory, and black pants.',
        'Tropical print men swim trunks with drawstring waistband and vibrant leaf and fruit designs.',
        'Vintage concert t-shirt featuring The Allman Brothers Band and Syria Mosque artwork.',
        'White t-shirt with colorful tomato illustrations in various shapes and sizes.'
    ]

    # Output CSV file path
    output_file = '/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data_llava_original.csv'

    # Create the CSV file
    create_csv(image_paths, predicted_captions_original, ground_truth_captions, output_file)
