#!/usr/bin/python
import os, sys
import argparse
import Image


"""
9 Patcher
Version 1.0 - Tue 3 May 2011

by Reimund Trost <reimund@code7.se>
<http://lumens.se/9-patcher/>

Requires Python Image Library and argparse.
"""
def main(argv=None):
	if argv is None:
		argv = sys.argv

	parser = argparse.ArgumentParser(description='Make 9 patch images.')
	parser.add_argument('-t', metavar='start,end', nargs='+', help='black pixels in top margin.')
	parser.add_argument('-r', metavar='start,end', nargs='+', help='black pixels in right margin.')
	parser.add_argument('-b', metavar='start,end', nargs='+', help='black pixels in bottom margin.')
	parser.add_argument('-l', metavar='start,end', nargs='+', help='black pixels in left margin.')
	parser.add_argument('-i', metavar='input', required=True, help='input graphic file or directory')
	parser.add_argument('-o', metavar='output', help='output graphic file or directory')
	parser.add_argument('-v', action='store_true', help='verbose output')

	args = vars(parser.parse_args())

	if (args['t'] == None and args['r'] == None
			and args['b'] == None and args['l'] == None):
		print 'No patches defined. There\'s nothing for me to do.'
	else:
		make_nine_patch(args)


def make_nine_patch(args):
	if (os.path.isdir(args['i'])):
		input_files = [args['i'] + '/' + x for x in os.listdir(args['i'])]
	else:
		input_files = [args['i']]

	for file in input_files:
		try:
			im = Image.open(file, 'r')
			(width, height) = im.size
			out_im = Image.new('RGBA', (width + 2, height + 2), (255,255,255,0))
			out_im.paste(im, (1, 1))
			pixels = out_im.load()
		except IOError:
			print ''.join(['Could not read ', file, '.']) 
			return
		
		try:
			draw_patches(args['t'], 'top', pixels, width, height)
			draw_patches(args['r'], 'right', pixels, width, height)
			draw_patches(args['b'], 'bottom', pixels, width, height)
			draw_patches(args['l'], 'left', pixels, width, height)
		except PatchError as e:
			print e
			return

		save_nine_patch(out_im, file, args['i'], args['o'], args['v'])


# Saves the specified image to the location indicated by the command line arguments.
def save_nine_patch(im, file, input, output, verbose):
	if (input == None):
		outfile = ninify(file)
	else:
		if (output == None):
			if (os.path.isdir(input)):
				output_dir = ninify(input)
				mkdir(output_dir)
				outfile = ''.join([output_dir, '/', ninify(file)])
			else:
				outfile = ninify(file)
		#elif (os.path.isdir(output)):
			#outfile = ''.join([output, '/', ninify(file)])
		else:
			if (os.path.isdir(input)):
				mkdir(output)
				outfile = ''.join([output, '/', ninify(file)])
			else:
				outfile = output

	try: 
		im.save(outfile, 'png')
		if (verbose):
			print ''.join(['Wrote \'', outfile, '\'.'])
	except IOError:
		print ''.join(['Could not create output file \'', outfile, '\'.'])


# Draws the black pixels on the specified patches.
def draw_patches(patches, edge, pixels, width, height):
	if patches == None:
		return
	
	range_end = str(width - 1) if (edge == 'top' or edge == 'bottom') else str(height - 1)
	y = 0 if (edge == 'top') else height + 1
	x = 0 if (edge == 'left') else width + 1

	for patch in patches:
		try:
			(position,length) = patch.split(',')
			for p in range(int(position), int(length) + 1):
				error_msg = ''.join([ 'A ', edge, ' patch region exceeds the image dimensions. ', edge.title(), ' patches must be within the range 0-', range_end, '.'])

				if (edge == 'top' or edge == 'bottom'):
					if (p + 1 > width):
						raise PatchError(error_msg)
					pixels[p + 1, y] = (0, 0, 0, 255)
				else:
					if (p + 1 > height):
						raise PatchError(error_msg)
					pixels[x, p + 1] = (0, 0, 0, 255)
					
		except ValueError:
			raise PatchError('Patch regions must be specified as integer pairs.')


# Adds a 9 to the specified filename, eg myfile.png -> myfile.9.png.
def ninify(path):
	head, tail = os.path.split(path)
	base, ext = os.path.splitext(tail)
	return ''.join([base, '.9', ext])
	

# Makes a directory only if it doesn't already exist.
def mkdir(name):
	if not os.path.exists(name):
		os.makedirs(name)


class PatchError(Exception):
    pass


if __name__ == "__main__":
    sys.exit(main())

