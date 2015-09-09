__kernel void AutoAudio(__global float* output)
{
	unsigned int id;
	float x;

	id = get_global_id(0);
	
	x = (float)id;
	
	output[id] = <FUNCTION>;
}